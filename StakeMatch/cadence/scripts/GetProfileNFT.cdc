import ProfileNFT from 0xf8d6e0586b0a20c7
import NonFungibleToken from 0xf8d6e0586b0a20c7

pub fun main(address: Address, id: UInt64): ProfileNFT.NFT? {
    // Get the public collection capability
    let collection = getAccount(address)
        .getCapability<&{NonFungibleToken.CollectionPublic}>(
            /public/ProfileNFTCollection
        )
        .borrow() ?? panic("Could not borrow ProfileNFT collection")
    
    // Get the specific NFT
    if let nft = collection.borrowNFT(id: id) as &ProfileNFT.NFT? {
        return nft
    }
    
    return nil
}
