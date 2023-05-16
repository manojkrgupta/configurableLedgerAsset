package com.r3.developers.configurableInstrument.requests

import net.corda.v5.base.types.MemberX500Name
import java.util.UUID

data class TransferRequest(val to: MemberX500Name,
                           val id: UUID,
                           val quantity: Int?=null
)