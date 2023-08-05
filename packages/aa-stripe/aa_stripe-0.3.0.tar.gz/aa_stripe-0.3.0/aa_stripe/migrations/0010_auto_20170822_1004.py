# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-22 10:04
from __future__ import unicode_literals

from decimal import Decimal

import django.db.models.deletion
import jsonfield.fields
import stripe
from django.db import migrations, models

from aa_stripe.settings import stripe_settings
from aa_stripe.utils import timestamp_to_timezone_aware_date


def migrate_subcription(apps, schema_editor):
    StripeSubscription = apps.get_model("aa_stripe", "StripeSubscription")
    StripeCoupon = apps.get_model("aa_stripe", "StripeCoupon")
    stripe.api_key = stripe_settings.API_KEY

    for subscription in StripeSubscription.objects.exclude(coupon_code=""):
        if StripeCoupon.objects.filter(coupon_id=subscription.coupon_code, is_deleted=False).exists():
            # do not allow duplicates
            continue

        try:
            stripe_coupon = stripe.Coupon.retrieve(id=subscription.coupon_code)
        except stripe.error.InvalidRequestError:
            print("Coupon {} does not exist, cannot migrate".format(subscription.coupon_code))
            continue

        fields = {
            "amount_off", "currency", "duration", "duration_in_months", "livemode", "max_redemptions",
            "percent_off", "redeem_by", "times_redeemed", "valid", "metadata", "created"
        }
        update_data = {key: stripe_coupon[key] for key in fields}
        update_data["created"] = timestamp_to_timezone_aware_date(stripe_coupon.get("created"))
        update_data["amount_off"] = Decimal(update_data["amount_off"]) / 100
        coupon = StripeCoupon.objects.create(coupon_id=stripe_coupon.get("id"), is_created_at_stripe=True,
                                             **update_data)
        subscription.coupon = coupon
        subscription.save()


class Migration(migrations.Migration):

    dependencies = [
        ('aa_stripe', '0009_auto_20170725_1205'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('stripe_response', jsonfield.fields.JSONField(default=dict)),
                ('coupon_id', models.CharField(help_text='Identifier for the coupon', max_length=255)),
                ('amount_off', models.DecimalField(decimal_places=2, max_digits=10, blank=True, help_text='Amount (in the currency specified) that will be taken off the subtotal ofany invoices for this customer.', null=True)),
                ('currency', models.CharField(default='usd', max_length=3, null=True, blank=True, help_text='If amount_off has been set, the three-letter ISO code for the currency of the amount to take off.', choices=[('usd', 'USD'), ('aed', 'AED'), ('afn', 'AFN'), ('all', 'ALL'), ('amd', 'AMD'), ('ang', 'ANG'), ('aoa', 'AOA'), ('ars', 'ARS'), ('aud', 'AUD'), ('awg', 'AWG'), ('azn', 'AZN'), ('bam', 'BAM'), ('bbd', 'BBD'), ('bdt', 'BDT'), ('bgn', 'BGN'), ('bif', 'BIF'), ('bmd', 'BMD'), ('bnd', 'BND'), ('bob', 'BOB'), ('brl', 'BRL'), ('bsd', 'BSD'), ('bwp', 'BWP'), ('bzd', 'BZD'), ('cad', 'CAD'), ('cdf', 'CDF'), ('chf', 'CHF'), ('clp', 'CLP'), ('cny', 'CNY'), ('cop', 'COP'), ('crc', 'CRC'), ('cve', 'CVE'), ('czk', 'CZK'), ('djf', 'DJF'), ('dkk', 'DKK'), ('dop', 'DOP'), ('dzd', 'DZD'), ('egp', 'EGP'), ('etb', 'ETB'), ('eur', 'EUR'), ('fjd', 'FJD'), ('fkp', 'FKP'), ('gbp', 'GBP'), ('gel', 'GEL'), ('gip', 'GIP'), ('gmd', 'GMD'), ('gnf', 'GNF'), ('gtq', 'GTQ'), ('gyd', 'GYD'), ('hkd', 'HKD'), ('hnl', 'HNL'), ('hrk', 'HRK'), ('htg', 'HTG'), ('huf', 'HUF'), ('idr', 'IDR'), ('ils', 'ILS'), ('inr', 'INR'), ('isk', 'ISK'), ('jmd', 'JMD'), ('jpy', 'JPY'), ('kes', 'KES'), ('kgs', 'KGS'), ('khr', 'KHR'), ('kmf', 'KMF'), ('krw', 'KRW'), ('kyd', 'KYD'), ('kzt', 'KZT'), ('lak', 'LAK'), ('lbp', 'LBP'), ('lkr', 'LKR'), ('lrd', 'LRD'), ('lsl', 'LSL'), ('mad', 'MAD'), ('mdl', 'MDL'), ('mga', 'MGA'), ('mkd', 'MKD'), ('mmk', 'MMK'), ('mnt', 'MNT'), ('mop', 'MOP'), ('mro', 'MRO'), ('mur', 'MUR'), ('mvr', 'MVR'), ('mwk', 'MWK'), ('mxn', 'MXN'), ('myr', 'MYR'), ('mzn', 'MZN'), ('nad', 'NAD'), ('ngn', 'NGN'), ('nio', 'NIO'), ('nok', 'NOK'), ('npr', 'NPR'), ('nzd', 'NZD'), ('pab', 'PAB'), ('pen', 'PEN'), ('pgk', 'PGK'), ('php', 'PHP'), ('pkr', 'PKR'), ('pln', 'PLN'), ('pyg', 'PYG'), ('qar', 'QAR'), ('ron', 'RON'), ('rsd', 'RSD'), ('rub', 'RUB'), ('rwf', 'RWF'), ('sar', 'SAR'), ('sbd', 'SBD'), ('scr', 'SCR'), ('sek', 'SEK'), ('sgd', 'SGD'), ('shp', 'SHP'), ('sll', 'SLL'), ('sos', 'SOS'), ('srd', 'SRD'), ('std', 'STD'), ('svc', 'SVC'), ('szl', 'SZL'), ('thb', 'THB'), ('tjs', 'TJS'), ('top', 'TOP'), ('try', 'TRY'), ('ttd', 'TTD'), ('twd', 'TWD'), ('tzs', 'TZS'), ('uah', 'UAH'), ('ugx', 'UGX'), ('uyu', 'UYU'), ('uzs', 'UZS'), ('vnd', 'VND'), ('vuv', 'VUV'), ('wst', 'WST'), ('xaf', 'XAF'), ('xcd', 'XCD'), ('xof', 'XOF'), ('xpf', 'XPF'), ('yer', 'YER'), ('zar', 'ZAR'), ('zmw', 'ZMW')])),
                ('duration', models.CharField(choices=[('forever', 'forever'), ('once', 'once'), ('repeating', 'repeating')], help_text='Describes how long a customer who applies this coupon will get the discount.', max_length=255)),
                ('duration_in_months', models.PositiveIntegerField(blank=True, help_text='If duration is repeating, the number of months the coupon applies.Null if coupon duration is forever or once.', null=True)),
                ('livemode', models.BooleanField(default=False, help_text='Flag indicating whether the object exists in live mode or test mode.')),
                ('max_redemptions', models.PositiveIntegerField(blank=True, help_text='Maximum number of times this coupon can be redeemed, in total, before it is no longer valid.', null=True)),
                ('metadata', jsonfield.fields.JSONField(default=dict, help_text='Set of key/value pairs that you can attach to an object. It can be useful forstoring additional information about the object in a structured format.')),
                ('percent_off', models.PositiveIntegerField(blank=True, help_text='Percent that will be taken off the subtotal of any invoicesfor this customer for the duration ofthe coupon. For example, a coupon with percent_off of 50 will make a $100 invoice $50 instead.', null=True)),
                ('redeem_by', models.DateTimeField(blank=True, help_text='Date after which the coupon can no longer be redeemed.', null=True)),
                ('times_redeemed', models.PositiveIntegerField(default=0, help_text='Number of times this coupon has been applied to a customer.')),
                ('valid', models.BooleanField(default=False, help_text='Taking account of the above properties, whether this coupon can still be applied to a customer.')),
                ('created', models.DateTimeField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_created_at_stripe', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='stripesubscription',
            old_name='coupon',
            new_name='coupon_code',
        ),
        migrations.AddField(
            model_name='stripesubscription',
            name='coupon',
            field=models.ForeignKey(blank=True, help_text='https://stripe.com/docs/api/python#create_subscription-coupon', null=True, on_delete=django.db.models.deletion.SET_NULL, to='aa_stripe.StripeCoupon'),
        ),
        migrations.RunPython(
            code=migrate_subcription,
            hints={'target_db': 'default'}
        ),
        migrations.RemoveField(
            model_name='stripesubscription',
            name='coupon_code'
        )
    ]
