package com.r3.developers.configurableInstrument.query

import com.r3.developers.configurableInstrument.states.Instrument
import net.corda.v5.application.flows.CordaInject
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.utxo.UtxoLedgerService
import net.corda.v5.application.flows.ClientRequestBody
import net.corda.v5.application.flows.ClientStartableFlow
import java.security.PublicKey
import java.util.*
import kotlin.collections.ArrayList
import kotlin.collections.HashMap
import kotlin.collections.LinkedHashMap

// Data class to hold the Flow results.
// The state(s) cannot be returned directly as the JsonMarshallingService can only serialize simple classes
// that the underlying Jackson serializer recognises, hence creating a DTO style object which consists only of Strings
// and a UUID. It is possible to create custom serializers for the JsonMarshallingService, but this is beyond the scope
// of this simple example.
data class ListInstrumentResult(
    val id: UUID,
    val name: String,
    val owner: String,
    val issuer: String,
    val quantity: Int?,
    val transferable: Boolean,
    val expiry: Date?,
    val verifiable: Boolean,
    val attributes: LinkedHashMap<String, String>
    )

class ListInstrument : ClientStartableFlow{

    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService

    @CordaInject
    lateinit var utxoLedgerService: UtxoLedgerService

    @Suspendable
    override fun call(requestBody: ClientRequestBody): String {

        var states = utxoLedgerService.findUnconsumedStatesByType(Instrument::class.java)

        val results = states.map {
            ListInstrumentResult(
                it.state.contractState.id,
                it.state.contractState.name,
                it.state.contractState.owner.toString(),
                it.state.contractState.issuer.toString(),
                it.state.contractState.quantity,
                it.state.contractState.transferable,
                it.state.contractState.expiry,
                it.state.contractState.verifiable,
                it.state.contractState.attributes,
            ) }

        // Uses the JsonMarshallingService's format() function to serialize the DTO to Json.
        return jsonMarshallingService.format(results)
    }
}

/*
RequestBody for triggering the flow via http-rpc:
{
    "clientRequestId": "list-1",
    "flowClassName": "com.r3.developers.csdetemplate.configurableInstrument.query.ListInstrument",
    "requestBody": {}
}
*/
