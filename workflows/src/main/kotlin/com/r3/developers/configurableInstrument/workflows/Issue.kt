package com.r3.developers.configurableInstrument.workflows

import com.r3.developers.configurableInstrument.contracts.InstrumentContract
import com.r3.developers.configurableInstrument.requests.IssueRequest
import com.r3.developers.configurableInstrument.states.Instrument
import net.corda.v5.application.flows.*
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.application.membership.MemberLookup
import net.corda.v5.application.messaging.FlowMessaging
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.common.NotaryLookup
import net.corda.v5.ledger.utxo.UtxoLedgerService
import org.slf4j.LoggerFactory
import java.time.Instant
import java.time.temporal.ChronoUnit
import java.util.*

@InitiatingFlow(protocol = "Issue-Configurable-Instrument")
class Issue : ClientStartableFlow {

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
        val request = requestBody.getRequestBodyAs<IssueRequest>(jsonMarshallingService, IssueRequest::class.java)

        // Retrieve the notaries public key (this will change)
        val notaryInfo = notaryLookup.notaryServices.single()
        val notaryKey = memberLookup.lookup().single {
            it.memberProvidedContext["corda.notary.service.name"] == notaryInfo.name.toString()
        }.ledgerKeys.first()

        val issuer = memberLookup.myInfo()

        val owner = memberLookup.lookup(request.to)
            ?: throw IllegalArgumentException("The owner ${request.to} does not exist within the network")

        if (request.quantity == 0) {
            throw IllegalArgumentException("Quantity can be Null/None, but cannot be zero.")
        }
        val session = flowMessaging.initiateFlow(request.to)
        log.info("1) Issue -- Issuing ${request.name} to ${session.counterparty.toString()}")

        session.send("${request.name}")
        session.send(issuer.name)
        val response = session.receive(String::class.java)

        log.info("3) Issue -- Response received '$response' from ${session.counterparty.toString()}")

        // Building the output state
        val state = Instrument(
            id = request.id,
            name = request.name,
            owner = owner.name,
            issuer = issuer.name,
            quantity = request.quantity,
            transferable = request.transferable,
            expiry = request.expiry,
            verifiable = request.verifiable,
            attributes =request.attributes,
            participants = listOf(issuer.ledgerKeys.first(), owner.ledgerKeys.first())
        )

        // Create the transaction
        @Suppress("DEPRECATION")
        val transaction = utxoLedgerService.createTransactionBuilder()
            .setNotary(notaryInfo.name)
            .addOutputState(state)
            .addCommand(InstrumentContract.Issue())
            .setTimeWindowUntil(Instant.now().plus(1, ChronoUnit.DAYS))
            .addSignatories(listOf(issuer.ledgerKeys.first(), owner.ledgerKeys.first()))
            .toSignedTransaction()

        return try {
            // Send the transaction and state to the counterparty and let them sign it
            // Then notarise and record the transaction in both parties' vaults.
            utxoLedgerService.finalize(transaction, listOf(session))
            return state.id.toString()
        } catch (e: Exception) {
            "Flow failed, message: ${e.message}"
        }
    }
}