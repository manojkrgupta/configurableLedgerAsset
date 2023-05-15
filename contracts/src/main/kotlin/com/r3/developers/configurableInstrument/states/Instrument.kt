package com.r3.developers.configurableInstrument.states

import com.r3.developers.configurableInstrument.contracts.InstrumentContract
import net.corda.v5.base.types.MemberX500Name
//import net.corda.v5.ledger.common.Party
import net.corda.v5.ledger.utxo.BelongsToContract
import net.corda.v5.ledger.utxo.ContractState
import net.corda.v5.membership.MemberInfo

import java.security.PublicKey
import java.util.*
import kotlin.collections.LinkedHashMap

@BelongsToContract(InstrumentContract::class)
class Instrument(
    val id: UUID,
    val owner: MemberX500Name,
    val issuer: MemberX500Name,
    val name: String,
    val quantity: Int?,
    val transferable: Boolean,
    val expiry: Date?,
    val verifiable: Boolean,
    val attributes: LinkedHashMap<String, String>,
    private val participants: List<PublicKey>
) : ContractState {

    override fun getParticipants(): List<PublicKey> {
        return participants
    }

    fun changeOwner(newOwner: MemberInfo, issuerMi: MemberInfo): Instrument {
        val participants = listOf(
            issuerMi.ledgerKeys.first(),
            newOwner.ledgerKeys.first())
//        val participants = listOf(issuer.owningKey, owner.owningKey)
        return Instrument(id, newOwner.name, issuer, name, quantity, transferable, expiry, verifiable, attributes, participants)
    }

    fun isFungible(): Boolean {
        return(quantity != null)
    }

    fun aggregateIfPossible(inst: Instrument): Instrument?{
        if (quantity == null)  return null
        if (name != inst.name) return null
        if (owner != inst.owner) return null
        if (issuer != inst.issuer) return null
        if (transferable != inst.transferable) return null
        if (expiry != inst.expiry) return null
        if (verifiable != inst.verifiable) return null
        if (attributes != inst.attributes) return null
        return(Instrument(UUID.randomUUID(), owner, issuer, name, (quantity + inst.quantity!!), transferable, expiry, verifiable, attributes, participants))
    }

    fun changeQuantity(totalQuantity: Int): Instrument {
//        val participants = listOf(issuer.owningKey, owner.owningKey)
        return Instrument(
            id,
            owner,
            issuer,
            name,
            totalQuantity,
            transferable,
            expiry,
            verifiable,
            attributes,
            participants
        )
    }

    fun partialTransfer(q: Int?, newOwner: MemberInfo, issuerMi: MemberInfo): MutableList<Instrument> {

        if ((quantity == null) or (q == null) or (q!! > quantity!!)) {throw IllegalArgumentException("Error 504")}
        val state1_old_owner = changeQuantity(quantity - q!!)
        val state2_new_owner = Instrument(
            UUID.randomUUID(),
            newOwner.name,
            issuer,
            name,
            q,
            transferable,
            expiry,
            verifiable,
            attributes,
            listOf(issuerMi.ledgerKeys.first(), newOwner.ledgerKeys.first())
        )
        return mutableListOf(state1_old_owner, state2_new_owner)
    }

    fun redeem(q: Int?): Instrument {
//        val participants = listOf(issuer.owningKey, owner.owningKey)
        val pending = quantity!! - q!!
        return Instrument(
            id,
            owner,
            issuer,
            name,
            pending,
            transferable,
            expiry,
            verifiable,
            attributes,
            participants
        )
    }

}