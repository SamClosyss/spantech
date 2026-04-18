-- disable pesapal payment provider
UPDATE payment_provider
   SET pesapal_consumer_key = NULL,
       pesapal_consumer_secret = NULL;