package com.r3.developers.configurableInstrument.contracts

import com.r3.developers.configurableInstrument.states.Instrument
import net.corda.v5.base.exceptions.CordaRuntimeException
//import net.corda.v5.ledger.common.Party
import net.corda.v5.ledger.utxo.Command
import net.corda.v5.ledger.utxo.Contract
import net.corda.v5.ledger.utxo.transaction.UtxoLedgerTransaction
import org.slf4j.LoggerFactory
import java.security.PublicKey
import java.util.*
import kotlin.collections.ArrayList
import kotlin.collections.HashMap

class InstrumentContract: Contract {

    private companion object {
        val log = LoggerFactory.getLogger(this::class.java.enclosingClass)
    }

    // Command Class used to indicate that the transaction should start a new chat.
    class Issue: Command
    // Command Class used to indicate that the transaction should append a new ChatState to an existing chat.
    class Transfer: Command

    class Aggregate: Command

    class Redeem: Command

    // verify() function is used to apply contract rules to the transaction.
    override fun verify(transaction: UtxoLedgerTransaction) {

        // Ensures that there is only one command in the transaction
        val command = transaction.commands.singleOrNull() ?: throw CordaRuntimeException("Requires a single command.")

        // Switches case based on the command
        when(command) {
            // Rules applied only to transactions with the Issue Command.
            is Issue -> {
                "When command is Issue there should be no input states." using (transaction.inputContractStates.isEmpty())
                "When command is Issue there should be one and only one output state." using (transaction.outputContractStates.size == 1)
                // Applies a universal constraint (applies to all transactions irrespective of command)
                "The output state should have two and only two participants." using {
                    val output = transaction.outputContractStates.first() as Instrument
                    output.participants.size== 2
                }

            }
            // Rules applied only to transactions with the Transfer Command.
            is Transfer -> {
                "When command is Transfer there should be one and only one input state." using (transaction.inputContractStates.size == 1)
//                "When command is Transfer there should be one and only one output state." using (transaction.outputContractStates.size == 1)
                val input = transaction.inputContractStates.single() as Instrument
                transaction.outputContractStates.map{it as Instrument }.forEach{ output ->
                    "When command is Transfer, name must not change." using (input.name == output.name)
                    "When command is Transfer, transferable must not change." using (input.transferable == output.transferable)
                    "When command is Transfer, expiry must not change." using (input.expiry == output.expiry)
                    "When command is Transfer, verifiable must not change." using (input.verifiable == output.verifiable)
                    "When command is Transfer, attributes must not change." using (input.attributes == output.attributes)
                    if (! input.isFungible()){
                        "When command is Transfer and instrument is not fungible, then quantity must not change." using (input.quantity == output.quantity)
                    }
                    // Applies a universal constraint (applies to all transactions irrespective of command)
                    "The output state should have two and only two participants." using (output.participants.size== 2)

//                "When command is Transfer, participants must not change." using (input.participants.toSet().intersect(output.participants.toSet()).size == 2)
                }

                val output = transaction.outputContractStates.first() as Instrument
//                "Action Transfer, but new owner is same as old owner" using(input.owner != output.owner)
                "Instrument is not transferable." using (input.transferable)
//                "When command is Transfer, id must not change." using (input.id == output.id)
            }
            is Aggregate -> {

            }
            is Redeem -> {
                // Applies a universal constraint (applies to all transactions irrespective of command)
//                "The output state should have two and only two participants." using {
//                    val output = transaction.outputContractStates.first() as Instrument
//                    output.participants.size== 2
//                }
            }
            else -> {
                throw CordaRuntimeException("Command not allowed.")
            }
        }
    }

    // Helper function to allow writing constraints in the Corda 4 '"text" using (boolean)' style
    private infix fun String.using(expr: Boolean) {
        if (!expr) throw CordaRuntimeException("Failed requirement: $this")
    }

    // Helper function to allow writing constraints in '"text" using {lambda}' style where the last expression
    // in the lambda is a boolean.
    private infix fun String.using(expr: () -> Boolean) {
        if (!expr.invoke()) throw CordaRuntimeException("Failed requirement: $this")
    }
}