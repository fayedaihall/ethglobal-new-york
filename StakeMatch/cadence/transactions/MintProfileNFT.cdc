import ProfileNFT from 0xf8d6e0586b0a20c7
import NonFungibleToken from 0xf8d6e0586b0a20c7

transaction(
    name: String,
    bio: String,
    profilePhoto: String,  // IPFS hash for profile photo
    coverPhoto: String     // IPFS hash for cover photo
) {
    // The account that will receive the NFT
    let recipient: &{NonFungibleToken.Collection}
    
    // Reference to the ProfileNFT contract
    let profileNFT: &ProfileNFT
    
    prepare(acct: AuthAccount) {
        // Get the ProfileNFT contract reference
        self.profileNFT = acct.borrow<&ProfileNFT>(from: /storage/ProfileNFT)
            ?? panic("Could not borrow ProfileNFT contract")
        
        // Get or create the recipient's collection
        if acct.borrow<&{NonFungibleToken.Collection}>(from: /storage/ProfileNFTCollection) == nil {
            // Create a new empty collection
            let collection <- ProfileNFT.createEmptyCollection()
            
            // Store it in the account
            acct.save(<-collection, to: /storage/ProfileNFTCollection)
            
            // Create a public capability for the collection
            acct.link<&{NonFungibleToken.CollectionPublic}>(
                /public/ProfileNFTCollection,
                target: /storage/ProfileNFTCollection
            )
        }
        
        // Get the recipient's collection
        self.recipient = acct.borrow<&{NonFungibleToken.Collection}>(
            from: /storage/ProfileNFTCollection
        ) ?? panic("Could not borrow ProfileNFT collection")
    }
    
    execute {
        // Mint the profile NFT
        let profileNFT <- self.profileNFT.mintProfile(
            name: name,
            bio: bio,
            profilePhoto: profilePhoto,
            coverPhoto: coverPhoto
        )
        
        // Deposit the NFT into the recipient's collection
        self.recipient.deposit(token: <-profileNFT)
        
        log("Profile NFT minted successfully!")
    }
}
