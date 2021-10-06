from imports import aws, cloudflare
from var import domain_name, cloudflare_zone_id
from s3 import PulumiBucket

cert = aws.acm.Certificate(
    "cert",
    domain_name=domain_name,
    validation_method="DNS",
    subject_alternative_names=["*." + domain_name],
)

cert_validation = aws.acm.CertificateValidation(
    "cert_validation", certificate_arn=cert.arn
)

s3_origin_id = "MyS3Origin"
s3_distribution = aws.cloudfront.Distribution(
    "s3Distribution",
    origins=[
        aws.cloudfront.DistributionOriginArgs(
            domain_name=PulumiBucket.bucket_regional_domain_name,
            origin_id=s3_origin_id,
        )
    ],
    enabled=True,
    default_root_object="index.html",
    aliases=[domain_name, "*." + domain_name],
    default_cache_behavior=aws.cloudfront.DistributionDefaultCacheBehaviorArgs(
        allowed_methods=[
            "DELETE",
            "GET",
            "HEAD",
            "OPTIONS",
            "PATCH",
            "POST",
            "PUT",
        ],
        cached_methods=[
            "GET",
            "HEAD",
        ],
        target_origin_id=s3_origin_id,
        forwarded_values=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesArgs(
            query_string=False,
            cookies=aws.cloudfront.DistributionDefaultCacheBehaviorForwardedValuesCookiesArgs(
                forward="none",
            ),
        ),
        viewer_protocol_policy="allow-all",
        min_ttl=0,
        default_ttl=3600,
        max_ttl=86400,
    ),
    price_class="PriceClass_100",
    restrictions=aws.cloudfront.DistributionRestrictionsArgs(
        geo_restriction=aws.cloudfront.DistributionRestrictionsGeoRestrictionArgs(
            restriction_type="whitelist",
            locations=[
                "US",
                "CA",
                "GB",
                "DE",
                "RO",
            ],
        ),
    ),
    viewer_certificate=aws.cloudfront.DistributionViewerCertificateArgs(
        acm_certificate_arn=cert_validation.certificate_arn,
        ssl_support_method="sni-only",
        minimum_protocol_version="TLSv1",
    ),
)
