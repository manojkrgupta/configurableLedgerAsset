package com.r3.developers.configurableInstrument.requests

import net.corda.v5.base.types.MemberX500Name
import java.util.*
import kotlin.collections.ArrayList
import kotlin.collections.HashMap
import kotlin.collections.LinkedHashMap

data class IssueRequest(
    val id: UUID = UUID.randomUUID(),     // Issuer should specify this
    val to: MemberX500Name,
    val name: String, // Bond, Limited edition Sovereign Asset, College Degree, Bearer Check
    val quantity: Int?=null,
    val transferable: Boolean=true, // false for College Degree
    val expiry: Date?=null, // Maturity for Bond, No expiry for College Degree, Limited edition Sovereign Asset
    val verifiable: Boolean=true,
    val attributes: LinkedHashMap<String, String> = LinkedHashMap() // Default is blank
)