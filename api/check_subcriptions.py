# This module is meant to be run as a separate process, supposedly through the
# frequently used 'api.main' module.


# Step 1:
# Check what supscriptions exist that have:
#   -1: Not yet expired
#       OR
#   -2: auto_resub=true

# Step 2:
# Check whether these subscriptions have been properly
# deducted as transactions.

# Step 3:
# Add that subscription data into any month that does not
# have it registered as a transaction ("TRANSACTIONS").
