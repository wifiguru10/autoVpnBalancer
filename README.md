# autoVpnBalancer
Tag based autoVPN hub configuration/balancer for Spoke Networks. Just tag one as "golden" and that configuration is synced/shared across all other spokes

# Tags:
Golden Tag = 'golden' by default
TAG Names = [ 'AVB_GROUP1', 'AVB_GROUP2', 'AVB_GROUP3', 'AVB_GROUP4' ]

#To Use:
1. The script will "learn" what hubs a spoke uses and replicate it out to all members of it's "group"
2. Tag all the networks with a group tag, 'AVB_GROUP1' for example
3. Pick one of those networks as your golden/master with the correct hub configuration already configured, add the 'golden' tag to that network
4. You should have one golden network that has both the 'AVB_GROUP1' and 'golden', that network configuration (what hubs that spokes connect to) will be copied to every other network with the "AVB_GROUP1" only. 
5. Networks with multiple active TAG names will be ignored. Only one can be active for the script to work. 

