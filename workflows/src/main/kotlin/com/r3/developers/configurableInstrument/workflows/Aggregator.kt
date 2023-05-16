package com.r3.developers.configurableInstrument.workflows

import com.r3.developers.configurableInstrument.contracts.InstrumentContract
import com.r3.developers.configurableInstrument.states.Instrument
import net.corda.v5.application.flows.*
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.application.membership.MemberLookup
import net.corda.v5.application.messaging.FlowMessaging
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.base.types.MemberX500Name
import net.corda.v5.ledger.common.NotaryLookup
import net.corda.v5.ledger.utxo.StateAndRef
import net.corda.v5.ledger.utxo.UtxoLedgerService
import org.slf4j.LoggerFactory
import java.time.Instant
import java.time.temporal.ChronoUnit
import java.util.*
import kotlin.collections.HashMap


@InitiatingFlow(protocol = "Aggregator-Configurable-Instrument")
class Aggregator(private val name: String, private val issuer: MemberX500Name) : SubFlow<String> {

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

    fun canBeAggregated(states: List<StateAndRef<Instrument>>): Map<String, MutableList<StateAndRef<Instrument>>> {
        val aggregatedStates = HashMap<String, MutableList<StateAndRef<Instrument>>>()
//        states.groupingBy { }.aggregate(k, accumulator: List, )
        for (s in states){
            val key = s.state.contractState.name +
                    s.state.contractState.issuer +
                    s.state.contractState.owner +
                    s.state.contractState.transferable.toString() +
                    s.state.contractState.expiry.toString() +
                    s.state.contractState.verifiable.toString() +
                    s.state.contractState.attributes.toString()

            if (key in aggregatedStates) {
                aggregatedStates[key]!!.add(s)
            }else{
                aggregatedStates[key] = mutableListOf(s)
            }
            log.info("Aggregating -- key = ${key}, value=${aggregatedStates[key].toString()}")
        }
        return (aggregatedStates.filter { it.value.count() > 1 })
    }

    @Suspendable
    override fun call(): String {
        // Retrieve the notaries public key (this will change)
        val notaryInfo = notaryLookup.notaryServices.single()
        val notaryKey = memberLookup.lookup().single {
            it.memberProvidedContext["corda.notary.service.name"] == notaryInfo.name.toString()
        }.ledgerKeys.first()

        val ourIdentity = memberLookup.myInfo()
//        val issuer = memberLookup.lookup(issuer.state.contractState.issuer.name) ?: throw CordaRuntimeException("Original issuer not found")
        log.info("Aggregating instrument='$name' from issuer='${issuer}'")

        val issuerSession = flowMessaging.initiateFlow(issuer)

        val unconsumedStates = utxoLedgerService.findUnconsumedStatesByType(Instrument::class.java)
            .filter{ stateAndRef -> stateAndRef.state.contractState.name == name &&
                    stateAndRef.state.contractState.owner == ourIdentity.name &&
                    stateAndRef.state.contractState.issuer == issuer &&
                    stateAndRef.state.contractState.quantity != null // Non null quantity is allowed to be aggregated
            }
        log.info("Aggregating -- unconsumedStates = ${unconsumedStates.toString()}")
        val canBeAggregated = canBeAggregated(unconsumedStates)
        log.info(canBeAggregated.toString())
        if (canBeAggregated.isEmpty()) {
            log.info("Aggregating -- nothing to aggregate")
            return "Nothing to aggregate"
        }

        canBeAggregated.entries.iterator().forEach {
            log.info("Aggregating -- key == ${it.key} value == ${it.value}")
//            log.info("val == id == " + it.value.map{it.state.contractState.id})
            log.info("Aggregating ")
            val totalQuantity = it.value.sumOf { s -> s.state.contractState.quantity!!.toInt() }
            val inputStates = it.value.map{ s -> s.ref}
            log.info("Aggregating -- list of input states -- ${inputStates} ")
            val outputState = it.value.first().state.contractState.changeQuantity(totalQuantity)
            // Create the transaction
            @Suppress("DEPRECATION")
            val transaction = utxoLedgerService.createTransactionBuilder()
                .setNotary(notaryInfo.name)
                .addInputStates(inputStates)
                .addOutputState(outputState)
                .addCommand(InstrumentContract.Aggregate())
                .setTimeWindowUntil(Instant.now().plus(1, ChronoUnit.DAYS))
                .addSignatories(listOf(ourIdentity.ledgerKeys.first()))
                .toSignedTransaction()

            try {
                // Send the transaction and state to the counterparty and let them sign it
                // Then notarise and record the transaction in both parties' vaults.
                val finalizedSignedTransaction = utxoLedgerService.finalize(transaction, listOf(issuerSession))
//            return(finalizedSignedTransaction.id.toString())

//                log.info(finalizedSignedTransaction.toString())
                return (outputState.id.toString())
            } catch (e: Exception) {
                "Flow failed, message: ${e.message}"
            }
        }

//        log.info("Aggregating " + input_states.map{ref -> "name="+ref.state.contractState.name.toString() +
//                "issuer=" + ref.state.contractState.issuer.toString() +
//                "quantity=" + ref.state.contractState.quantity})
//
//        log.info("Transfer request -- found the state id=${input_state.state.contractState.id}, " +
//                "name=${input_state.state.contractState.name} transferable=${input_state.state.contractState.transferable} " +
//                "expiry=${input_state.state.contractState.expiry}" +
//                "from ${ourIdentity.name} to ${request.to}")


        return "completed"
    }
}