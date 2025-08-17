# Profile NFT System

This system allows users to mint profile NFTs that store their bio and photo information as IPFS hashes.

## Features

- **Profile NFT Minting**: Users can mint profile NFTs with name, bio, profile photo, and cover photo
- **IPFS Integration**: Photos are stored as IPFS hashes for decentralized storage
- **Metadata Views**: NFTs support standard Flow metadata views for easy integration with wallets and marketplaces
- **Collection Management**: Users can manage their profile NFT collection

## How to Use

### 1. Deploy the Contract

First, deploy the ProfileNFT contract:

```bash
flow deploy
```

### 2. Mint a Profile NFT

Use the `MintProfileNFT` transaction to create your profile NFT:

```bash
flow transactions send cadence/transactions/MintProfileNFT.cdc \
  --arg String:"Your Name" \
  --arg String:"Your bio description here" \
  --arg String:"QmYourProfilePhotoIPFSHash" \
  --arg String:"QmYourCoverPhotoIPFSHash"
```

**Parameters:**

- `name`: Your display name
- `bio`: Your bio description
- `profilePhoto`: IPFS hash for your profile photo
- `coverPhoto`: IPFS hash for your cover photo

### 3. View Your Profile NFT Collection

To see all your profile NFTs:

```bash
flow scripts execute cadence/scripts/GetProfileNFTCollection.cdc \
  --arg Address:0xYourAddress
```

### 4. View a Specific Profile NFT

To view a specific profile NFT by ID:

```bash
flow scripts execute cadence/scripts/GetProfileNFT.cdc \
  --arg Address:0xYourAddress \
  --arg UInt64:1
```

## IPFS Integration

### Upload Photos to IPFS

1. **Using IPFS Desktop**: Drag and drop your images
2. **Using Pinata**: Upload via their web interface
3. **Using Infura IPFS**: Use their API or web interface

### Get IPFS Hash

After uploading, you'll get a hash like:

```
QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
```

Use this hash in the minting transaction.

## Contract Structure

### NFT Resource

- `id`: Unique identifier
- `metadata`: Contains name, bio, profilePhoto, coverPhoto
- `createdAt`: Timestamp when NFT was created

### Collection Resource

- Manages owned NFTs
- Supports standard NonFungibleToken operations
- Provides metadata views for wallets and marketplaces

## Events

- `ProfileMinted`: Emitted when a new profile NFT is created
- `Withdraw`: Emitted when an NFT is withdrawn
- `Deposit`: Emitted when an NFT is deposited

## Metadata Views

The ProfileNFT supports:

- `MetadataViews.Display`: Rich display information for wallets
- `MetadataViews.NFTView`: Basic NFT information

## Example Usage

```cadence
// Mint a profile NFT
let profileNFT <- ProfileNFT.mintProfile(
    name: "Alice",
    bio: "Blockchain developer and NFT enthusiast",
    profilePhoto: "QmProfilePhotoHash",
    coverPhoto: "QmCoverPhotoHash"
)

// Store in collection
collection.deposit(token: <-profileNFT)
```

## Security Notes

- Only the account owner can mint NFTs to their collection
- IPFS hashes should be verified before minting
- Consider using IPFS pinning services for reliable storage
