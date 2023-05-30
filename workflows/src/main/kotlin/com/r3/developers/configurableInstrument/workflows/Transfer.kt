package com.r3.developers.configurableInstrument.workflows

import com.r3.developers.configurableInstrument.contracts.InstrumentContract
import com.r3.developers.configurableInstrument.requests.TransferRequest
import com.r3.developers.configurableInstrument.states.Instrument
import net.corda.v5.application.flows.*
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.application.membership.MemberLookup
import net.corda.v5.application.messaging.FlowMessaging
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.base.exceptions.CordaRuntimeException
import net.corda.v5.ledger.common.NotaryLookup
import net.corda.v5.ledger.utxo.ContractState
import net.corda.v5.ledger.utxo.UtxoLedgerService
import org.slf4j.LoggerFactory
import java.time.Instant
import java.time.temporal.ChronoUnit
import java.util.*


@InitiatingFlow(protocol = "Transfer-Configurable-Instrument")
class Transfer : ClientStartableFlow {

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
        val request = requestBody.getRequestBodyAs<TransferRequest>(jsonMarshallingService, TransferRequest::class.java)
        val stateId = request.id
        val quantity = request.quantity

        // Retrieve the notaries public key (this will change)
        val notaryInfo = notaryLookup.notaryServices.single()
        val notaryKey = memberLookup.lookup().single {
            it.memberProvidedContext["corda.notary.service.name"] == notaryInfo.name.toString()
        }.ledgerKeys.first()

//        val notary = MemberLookup.look
//        val notary = Party(notaryInfo.name, notaryKey)

        val ourIdentity = memberLookup.myInfo()
        log.info("Transfer request of instrument id=$stateId, from ${ourIdentity.name} to ${request.to} quantity='$quantity'")

        val newOwner = memberLookup.lookup(request.to)
            ?: throw IllegalArgumentException("New Owner does not exist in the network")

        val inputState = utxoLedgerService.findUnconsumedStatesByType(Instrument::class.java)
            .firstOrNull { stateAndRef -> stateAndRef.state.contractState.id == stateId && stateAndRef.state.contractState.owner == ourIdentity.name}
            ?: throw IllegalArgumentException("Not able to find a owning state with id $stateId")

        // Create the transaction
        @Suppress("DEPRECATION")
        var outputList = mutableListOf<ContractState>()
        var issuerMi = memberLookup.lookup(inputState.state.contractState.issuer)?: throw IllegalArgumentException("Issuer does not exist in the network")

        log.info("Transfer request of instrument id=$stateId, from ${ourIdentity.name} to ${request.to} quantity='$quantity' input state quantity is '${inputState.state.contractState.quantity}'")

        var return_val: UUID
        if (listOf(null, inputState.state.contractState.quantity).contains(quantity)) {// if quantity(q) is null or same as transfer quantity(transfer all)
//            log.info("transfer requested quantity=$quantity, input state quantity=${inputState.state.contractState.quantity} -- going for changeOwner call")
            // Complete transfer(transfer all)
            outputList.add(inputState.state.contractState.changeOwner(newOwner, issuerMi))
            return_val = (outputList[0] as Instrument).id
        }else{
//            log.info("transfer requested quantity=$quantity, input state quantity=${inputState.state.contractState.quantity} -- going for partialTransfer call")
            // Partial transfer(transfer small set)
            outputList = inputState.state.contractState.partialTransfer(quantity, newOwner, issuerMi).toMutableList()
            return_val = (outputList[1] as Instrument).id
        }

        log.info("Transfer request -- found the state id=${inputState.state.contractState.id}, " +
                "name=${inputState.state.contractState.name} transferable=${inputState.state.contractState.transferable} " +
                "expiry=${inputState.state.contractState.expiry}" +
                "from ${ourIdentity.name} to ${request.to}")
        val issuer = memberLookup.lookup(inputState.state.contractState.issuer) ?: throw CordaRuntimeException("Original issuer not found")


        // Create the transaction
        @Suppress("DEPRECATION")
        val transactionBuilder = utxoLedgerService.createTransactionBuilder()
            .setNotary(notaryInfo.name)
            .addInputStates(inputState.ref)
            .addOutputStates(/* contractStates = */ outputList)
//            .addOutputStates(s0, s1)

//         if (s1 != null){
//             transaction_builder.addOutputState(s1)
//         }

        val transaction = transactionBuilder.addCommand(InstrumentContract.Transfer())
            .setTimeWindowUntil(Instant.now().plus(1, ChronoUnit.DAYS))
            .addSignatories(listOf(ourIdentity.ledgerKeys.first(), newOwner.ledgerKeys.first()))
            .toSignedTransaction()

        val newOwnerSession = flowMessaging.initiateFlow(request.to)
        val issuerSession = flowMessaging.initiateFlow(inputState.state.contractState.issuer)

        newOwnerSession.send(inputState.state.contractState.name)
        newOwnerSession.send(inputState.state.contractState.issuer)
        issuerSession.send(inputState.state.contractState.name) // not needed
        issuerSession.send(inputState.state.contractState.issuer) // not needed
        return try {
            // Send the transaction and state to the counterparty and let them sign it
            // Then notarise and record the transaction in both parties' vaults.
            val finalizedSignedTransaction = utxoLedgerService.finalize(transaction, listOf(newOwnerSession, issuerSession))

// Auto Aggregator -- Stopping
// Aggregator at the initiator
//            flowEngine.subFlow(Aggregator(inputState.state.contractState.name, inputState.state.contractState.issuer))
//            return(finalizedSignedTransaction.toString())
            return return_val.toString()
        } catch (e: Exception) {
            "Flow failed, message: ${e.message}"
        }
    }
}