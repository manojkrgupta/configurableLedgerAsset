package com.r3.developers.configurableInstrument.workflows

import com.r3.developers.configurableInstrument.contracts.InstrumentContract
import com.r3.developers.configurableInstrument.requests.RedeemRequest
import com.r3.developers.configurableInstrument.states.Instrument
import net.corda.v5.application.flows.*
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.application.membership.MemberLookup
import net.corda.v5.application.messaging.FlowMessaging
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.base.exceptions.CordaRuntimeException
import net.corda.v5.ledger.common.NotaryLookup
import net.corda.v5.ledger.utxo.UtxoLedgerService
import org.slf4j.LoggerFactory
import java.time.Instant
import java.time.temporal.ChronoUnit

@InitiatingFlow(protocol = "Redeem-Configurable-Instrument")
class Redeem : ClientStartableFlow {

    private companion object {
        val log = LoggerFactory.getLogger(this::class.java.enclosingClass)
    }

    @CordaInject
    lateinit var flowMessaging: FlowMessaging

    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService

    @CordaInject
    lateinit var memberLookup: MemberLookup

    @CordaInject
    lateinit var notaryLookup: NotaryLookup

    @CordaInject
    lateinit var utxoLedgerService: UtxoLedgerService

    // FlowEngine service is required to run SubFlows.
    @CordaInject
    lateinit var flowEngine: FlowEngine

    @Suspendable
    override fun call(requestBody: ClientRequestBody): String {
        val request = requestBody.getRequestBodyAs<RedeemRequest>(jsonMarshallingService, RedeemRequest::class.java)
        val stateId = request.id
        val quantity = request.quantity

        // Retrieve the notaries public key (this will change)
        val notaryInfo = notaryLookup.notaryServices.single()
        val notaryKey = memberLookup.lookup().single {
            it.memberProvidedContext["corda.notary.service.name"] == notaryInfo.name.toString()
        }.ledgerKeys.first()

        val ourIdentity = memberLookup.myInfo()
        log.info("Redeem request of instrument id=$stateId quantity=$quantity ourIdentity=$ourIdentity ")

        utxoLedgerService.findUnconsumedStatesByType(Instrument::class.java)
            .forEach { stateAndRef ->
                log.info(
                    "Quering for Redeem -- id = ${stateAndRef.state.contractState.id}, " +
                            "owner=${stateAndRef.state.contractState.owner}, " +
                            "issuer = ${stateAndRef.state.contractState.issuer}" +
                            "ourIdentity= $ourIdentity match ==>" + (ourIdentity.name == stateAndRef.state.contractState.owner) +
                            (ourIdentity.name == stateAndRef.state.contractState.issuer)
                )
        }

        val inputState = utxoLedgerService.findUnconsumedStatesByType(Instrument::class.java)
            .firstOrNull { stateAndRef ->
                stateAndRef.state.contractState.id == stateId &&
                        (stateAndRef.state.contractState.owner == ourIdentity.name ||
                                stateAndRef.state.contractState.issuer == ourIdentity.name
                                )
            }
            ?: throw IllegalArgumentException("Not able to find a owning state with id $stateId")

        log.info("Redeem request -- found the state id=${inputState.state.contractState.id}, " +
                "name=${inputState.state.contractState.name} transferable=${inputState.state.contractState.transferable} " +
                "expiry=${inputState.state.contractState.expiry} quantity=${inputState.state.contractState.quantity}" +
                "from ${ourIdentity.name}")

// Since Redeem is allowed by issuer as well as owner -- ouridentity can be either issuer or owner. -- hence we have to choose between issuer or owner as counterparty
        val issuer = memberLookup.lookup(inputState.state.contractState.issuer) ?: throw CordaRuntimeException("Original issuer not found")
        val owner = memberLookup.lookup(inputState.state.contractState.owner) ?: throw CordaRuntimeException("Original owner not found")
        var counterParty = issuer
        if (ourIdentity == counterParty){
            counterParty = owner
        }

//        val issuer = memberLookup.myInfo().let { Party(it.name, it.ledgerKeys.first()) }

        // Create the transaction
        @Suppress("DEPRECATION")
        val transactionBuilder = utxoLedgerService.createTransactionBuilder()
            .setNotary(notaryInfo.name)
            .addInputStates(inputState.ref)

        if (quantity != null) {
            if (inputState.state.contractState.quantity == null){
                throw IllegalArgumentException("Redeem quantity requested is $quantity, whereas quantity in instrument id $stateId is null")
            }else if (inputState.state.contractState.quantity!! < quantity!!){
                throw IllegalArgumentException("Redeem quantity requested is $quantity, whereas quantity in instrument id $stateId is ${inputState.state.contractState.quantity} (less quantity)")
            }else if (inputState.state.contractState.quantity!! > quantity!!) {
                var outputState = inputState.state.contractState.redeem(quantity)
                transactionBuilder.addOutputState(outputState)
            }else if (inputState.state.contractState.quantity!! == quantity!!) {
//                var outputState = inputState.state.contractState.redeem(quantity) // redeem all. Quantity is zero.
//                transactionBuilder.addOutputState(outputState) // redeem all. Quantity is zero.
                // Nothing needs to be done. All getting consumed.
            }
        }

        val transaction = transactionBuilder.addCommand(InstrumentContract.Redeem())
            .setTimeWindowUntil(Instant.now().plus(1, ChronoUnit.DAYS))
            .addSignatories(listOf(counterParty.ledgerKeys.first(), ourIdentity.ledgerKeys.first()))
            .toSignedTransaction()

        val issuerSession = flowMessaging.initiateFlow(counterParty.name)

        issuerSession.send(inputState.state.contractState.name) // not needed
        issuerSession.send(inputState.state.contractState.id) // not needed
        return try {
            // Send the transaction and state to the counterparty and let them sign it
            // Then notarise and record the transaction in both parties' vaults.
            val finalizedSignedTransaction = utxoLedgerService.finalize(transaction, listOf(issuerSession))

            return(finalizedSignedTransaction.toString())
        } catch (e: Exception) {
            "Flow failed, message: ${e.message}"
        }
    }
}