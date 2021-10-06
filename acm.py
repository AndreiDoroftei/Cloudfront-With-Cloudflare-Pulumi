from os import name
from pulumi_cloudflare import zone
from imports import cloudflare
from cloudfront_distribution import s3_distribution, cert
from var import cloudflare_zone_id, domain_name

acm = cloudflare.Record(
    "ACM",
    zone_id=cloudflare_zone_id,
    name=cert.domain_validation_options[0].resource_record_name,
    type=cert.domain_validation_options[0].resource_record_type,
    value=cert.domain_validation_options[0].resource_record_value,
    ttl=60,
)
domain_cname = cloudflare.Record(
    "Domain_Cname",
    zone_id=cloudflare_zone_id,
    name=domain_name,
    value=s3_distribution.domain_name,
    type="CNAME",
)

domain_cname_www = cloudflare.Record(
    "Domain_Cname_www",
    zone_id=cloudflare_zone_id,
    name="www",
    value=s3_distribution.domain_name,
    type="CNAME",
)
