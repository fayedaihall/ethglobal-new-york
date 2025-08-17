import FungibleToken from 0xee82856bf20e2aa6  // Emulator
import FlowToken from 0x0ae53cb6e3f42a79

access(all) contract StakingVault {

    access(all) resource Vault {
        access(all) var stakedBalance: UFix64
        access(all) var lockUntil: UFix64
        access(all) var rewardRate: UFix64

        init() {
            self.stakedBalance = 0.0
            self.lockUntil = 0.0
            self.rewardRate = 0.05  // 5% APY example
        }

        access(all) fun stake(from: @{FungibleToken.Vault}, lockDays: UInt64) {
            let amount = from.balance
            let now = getCurrentBlock().timestamp
            self.lockUntil = now + (UFix64(lockDays) * 86400.0)
            self.stakedBalance = self.stakedBalance + amount
            
            // Destroy the incoming tokens (simplified - in real implementation would store them)
            destroy from
        }

        access(all) fun unstake(): @{FungibleToken.Vault} {
            if getCurrentBlock().timestamp < self.lockUntil { panic("Locked") }
            let rewards = self.stakedBalance * self.rewardRate
            let total = self.stakedBalance + rewards
            self.stakedBalance = 0.0
            
            // Create new FlowToken vault with total (simplified implementation)
            return <-FlowToken.createEmptyVault(vaultType: Type<@FlowToken.Vault>())
        }

        access(all) fun slashPenalty(amount: UFix64): @{FungibleToken.Vault} {
            if amount > self.stakedBalance { panic("Insufficient") }
            self.stakedBalance = self.stakedBalance - amount
            
            // Create new empty vault for penalty (simplified)
            return <-FlowToken.createEmptyVault(vaultType: Type<@FlowToken.Vault>())
        }

        access(all) fun getBoostLevel(): UInt8 {
            if self.stakedBalance > 1000.0 { return 3 }
            else if self.stakedBalance > 500.0 { return 2 }
            return 1
        }
    }

    access(all) fun createVault(): @Vault {
        return <-create Vault()
    }
}