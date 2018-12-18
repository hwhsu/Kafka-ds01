
# 一個DTO（Data Transfer Object)的示範
class Taxidata:

    # 類別建構子
    def __init__(self, row_id=0, medallion='', hack_license='', vendor_id='',
                 payment_type='', fare_amount=0.0, surcharge=0.0, mta_tax=0.0,
                 tip_amount=0.0, tolls_amount=0.0, total_amount=0.0, rate_code=0,
                 pickup_datetime=None, dropoff_datetime=None, passenger_count=0,
                 trip_time_in_secs=0, trip_distance=0.0, pickup_longitude=0.0,
                 pickup_latitude=0.0, dropoff_longitude=0.0, dropoff_latitude=0.0,
                 credit_card=''):
        self.row_id = row_id
        self.medallion = medallion
        self.hack_license = hack_license
        self.vendor_id = vendor_id
        self.payment_type = payment_type
        self.fare_amount = fare_amount
        self.surcharge = surcharge
        self.mta_tax = mta_tax
        self.tip_amount = tip_amount
        self.tolls_amount = tolls_amount
        self.total_amount = total_amount
        self.rate_code = rate_code
        self.pickup_datetime = pickup_datetime
        self.dropoff_datetime = dropoff_datetime
        self.passenger_count = passenger_count
        self.trip_time_in_secs = trip_time_in_secs
        self.trip_distance = trip_distance
        self.pickup_longitude = pickup_longitude
        self.pickup_latitude = pickup_latitude
        self.dropoff_longitude = dropoff_longitude
        self.dropoff_latitude = dropoff_latitude
        self.credit_card = credit_card

