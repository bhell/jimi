# Possible discounts:
# - Node (administer inline with nodes)
# - Bulk amounts on nodes
# - User
# - Group of users
# - Order (this is more-or-less a voucher)
# - Shipping costs
# Possible amounts:
# - Percentage
# - Fixed amount
# Flag indicating if a discount can be combined with other discounts.
# Boolean "offer" to include in list of offers. Default to true if discount is at node level.
# Save all applied discounts when ordering in a ManyToMany relationship with Order.
