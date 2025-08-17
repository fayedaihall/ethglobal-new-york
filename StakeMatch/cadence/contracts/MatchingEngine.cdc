import ProfileNFT from 0xf8d6e0586b0a20c7  // Emulator address
import StakingVault from 0xf8d6e0586b0a20c7  // Emulator address
import FungibleToken from 0xee82856bf20e2aa6  // Emulator address

access(all) contract MatchingEngine {

    access(all) resource MatchSession {
        access(all) let userA: Address
        access(all) let userB: Address
        access(all) var lastInteractionA: UFix64
        access(all) var lastInteractionB: UFix64
        access(all) var ghostClaim: Address?
        access(all) var claimTimestamp: UFix64?
        access(all) let ghostWindow: UFix64  // 7 days
        access(all) let disputeWindow: UFix64  // 3 days
        access(all) let penaltyPct: UFix64  // 20%

        init(userA: Address, userB: Address) {
            self.userA = userA
            self.userB = userB
            self.lastInteractionA = getCurrentBlock().timestamp
            self.lastInteractionB = getCurrentBlock().timestamp
            self.ghostClaim = nil
            self.claimTimestamp = nil
            self.ghostWindow = 604800.0
            self.disputeWindow = 259200.0
            self.penaltyPct = 0.2
        }

        access(all) fun updateInteraction(user: Address) {
            if user == self.userA { self.lastInteractionA = getCurrentBlock().timestamp }
            else if user == self.userB { self.lastInteractionB = getCurrentBlock().timestamp }
            else { panic("Invalid user") }
        }

        access(all) fun initiateGhostClaim(claimer: Address) {
            if self.ghostClaim != nil { panic("Claim active") }
            let now = getCurrentBlock().timestamp
            let ghoster = claimer == self.userA ? self.userB : self.userA
            let lastInteraction = claimer == self.userA ? self.lastInteractionB : self.lastInteractionA
            if now - lastInteraction < self.ghostWindow { panic("Window not elapsed") }
            self.ghostClaim = claimer
            self.claimTimestamp = now
            // Note: Agent automation would need matchID context
        }

        access(all) fun disputeClaim(disputer: Address) {
            let now = getCurrentBlock().timestamp
            if self.ghostClaim == nil { panic("No claim") }
            if now - self.claimTimestamp! > self.disputeWindow { panic("Dispute passed") }
            if disputer != (self.ghostClaim == self.userA ? self.userB : self.userA) { panic("Invalid") }
            self.updateInteraction(user: disputer)
            self.ghostClaim = nil
            self.claimTimestamp = nil
        }

        access(all) fun setGhostClaim(claimer: Address?) {
            self.ghostClaim = claimer
        }

        access(all) fun setClaimTimestamp(timestamp: UFix64?) {
            self.claimTimestamp = timestamp
        }
    }

    access(all) resource Agent {
        access(all) fun automatePenalty(matchID: UInt64) {
            let sessionRef = MatchingEngine.getMatchSession(matchID: matchID) ?? panic("No session")
            let now = getCurrentBlock().timestamp
            if sessionRef.ghostClaim == nil { return }
            if now - sessionRef.claimTimestamp! <= sessionRef.disputeWindow { return }
            self.executePenaltyAction(session: sessionRef)
        }

        access(all) fun executePenaltyAction(session: &MatchSession) {
            let ghoster = session.ghostClaim == session.userA ? session.userB : session.userA
            let victim = session.ghostClaim!
            
            // For now, just emit an event since we can't easily access private vaults
            // In a real implementation, this would require proper capability management
            let penaltyAmount = 100.0 // Simplified penalty amount
            
            session.setGhostClaim(claimer: nil)
            session.setClaimTimestamp(timestamp: nil)
            emit PenaltyAutomated(ghoster: ghoster, amount: penaltyAmount)
        }
    }

    access(all) var matchSessions: @{UInt64: MatchSession}
    access(all) var nextMatchID: UInt64
    access(all) var agent: @Agent

    init() {
        self.matchSessions <- {}
        self.nextMatchID = 0
        self.agent <- create Agent()
    }

    access(all) fun createMatch(userA: Address, userB: Address): UInt64 {
        let matchID = self.nextMatchID
        self.nextMatchID = self.nextMatchID + 1
        let newSession <- create MatchSession(userA: userA, userB: userB)
        let oldSession <- self.matchSessions[matchID] <- newSession
        destroy oldSession
        return matchID
    }

    access(all) fun swipe(user: Address, targetProfileID: UInt64, like: Bool) {
        // Logic for swipes; integrate boost from stake
        // Simplified implementation without vault access for now
        let boost: UInt8 = 1 // Default boost level
        // Apply boost to visibility/swipes
        log("User swiped with boost level: ".concat(boost.toString()))
    }

    access(all) fun match(userA: Address, userB: Address) {
        // Confirm mutual likes, create session
        let matchID = self.createMatch(userA: userA, userB: userB)
        log("Match created with ID: ".concat(matchID.toString()))
    }

    access(all) fun getMatchSession(matchID: UInt64): &MatchSession? {
        return &self.matchSessions[matchID] as &MatchSession?
    }

    access(all) event PenaltyAutomated(ghoster: Address, amount: UFix64)
}
