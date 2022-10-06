// SPDX-License-Identifier: MIT
pragma solidity 0.8.11;


interface IAdvocateEnum {
    enum Level { SILVER, GOLD, PLATINUM, DIAMOND }
    enum ReserveObject {
        CUSTOMER_REWARD,
        PLATFORM_FEE,
        COMMUNITY_CAMPAIGN,
        QUARTER_REFERRAL_REWARD,
        ADVOCATE_REWARD
    }
}