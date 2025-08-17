import ProfileNFT from 0xf8d6e0586b0a20c7
import NonFungibleToken from 0xf8d6e0586b0a20c7

pub fun main(address: Address): [ProfileNFT.NFT] {
    // Get the public collection capability
    let collection = getAccount(address)
        .getCapability<&{NonFungibleToken.CollectionPublic}>(
            /public/ProfileNFTCollection
        )
        .borrow() ?? panic("Could not borrow ProfileNFT collection")
    
    // Get all NFT IDs in the collection
    let ids = collection.getIDs()
    
    // Get all NFTs
    let nfts: [ProfileNFT.NFT] = []
    
    for id in ids {
        if let nft = collection.borrowNFT(id: id) as &ProfileNFT.NFT? {
            nfts.append(nft)
        }
    }
    
    return nfts
}
