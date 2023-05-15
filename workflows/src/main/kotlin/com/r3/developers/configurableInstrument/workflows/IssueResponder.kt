package com.r3.developers.configurableInstrument.workflows

import net.corda.v5.application.flows.CordaInject
import net.corda.v5.application.flows.InitiatedBy
import net.corda.v5.application.flows.ResponderFlow
import net.corda.v5.application.messaging.FlowSession
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.base.types.MemberX500Name
import net.corda.v5.ledger.utxo.UtxoLedgerService
import org.slf4j.LoggerFactory

@InitiatedBy(protocol = "Issue-Configurable-Instrument")
class IssueResponder : ResponderFlow {

    private companion object {
        val log = LoggerFactory.getLogger(this::class.java.enclosingClass)
    }

    @CordaInject
    lateinit var utxoLedgerService: UtxoLedgerService

    @Suspendable
    override fun call(session: FlowSession) {
        val name = session.receive(String::class.java)
        val issuer = session.receive(MemberX500Name::class.java)
        log.info("Issue new Instrument -- name=$name issuer=$issuer from ${session.counterparty.toString()}")
        session.send("yahoo")

        // Receive, verify, validate, sign and record the transaction sent from the initiator
        utxoLedgerService.receiveFinality(session) { transaction ->
            log.info("transaction id == " + transaction.id.toString())
            /*
             * [receiveFinality] will automatically verify the transaction and its signatures before signing it.
             * However, just because a transaction is contractually valid doesn't mean we necessarily want to sign.
             * What if we don't want to deal with the counterparty in question, or the value is too high,
             * or we're not happy with the transaction's structure? [UtxoTransactionValidator] (the lambda created
             * here) allows us to define the additional checks. If any of these conditions are not met,
             * we will not sign the transaction - even if the transaction and its signatures are contractually valid.
             */

        }

// Auto Aggregator -- Stopping
//        log.info("Issue -- Aggregation -- ${name}, ${issuer.name}")
//        flowEngine.subFlow(Aggregator(name, issuer))

    }
}