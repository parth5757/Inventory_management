from celery import shared_task
from celery.utils.log import get_task_logger
import random
import string
from django.core.mail import send_mail
from django.core.cache import cache
from django.core.cache.backends.base import InvalidCacheBackendError

@shared_task(bind=True)
def test_fun(self):
    for i in range(10):
        print(i)
    return "Done"


def generate_otp():
    
    # Generate 4 or 5 random digits
    num_digits = random.choice([4, 5])
    digits = random.choices(string.digits, k=num_digits)
    
    # Generate 1 or 2 random alphabets
    num_alphabets = 6 - num_digits
    alphabets = random.choices(string.ascii_lowercase, k=num_alphabets)
    
    # Combine digits and alphabets
    otp_components = digits + alphabets
    
    # Shuffle to randomize the positions
    random.shuffle(otp_components)
    
    # Join to create the OTP
    otp = ''.join(otp_components)
    return otp

logger = get_task_logger(__name__)

# just for temporary checking not always to do.
def check_redis_connection():
    try:
        # Try setting and retrieving a value from Redis cache
        cache.set('connection_test', 'success', timeout=1)
        result = cache.get('connection_test')
        if result == 'success':
            logger.info("Connected to Redis successfully via Django cache!")
            return True
        else:
            logger.info("Failed to retrieve the test value from Redis cache.")
            return False
    except InvalidCacheBackendError as e:
        logger.info(f"Invalid cache backend configuration: {e}")
    except Exception as e:
        logger.info(f"Failed to connect to Redis: {e}")


@shared_task(bind=True)
def send_otp_handler(self, email):
    otp = generate_otp()
    if check_redis_connection():
        logger.info(f"Your OTP is {otp} & {email}")
        cache_timeout = 300  # 5 minutes in seconds

        # Store OTP and email cache
        cache_key = email
        logger.info("cache_key: ", cache_key)
        cache.set(cache_key, otp, timeout=cache_timeout)

        # Log debugging
        logger.info(f"Your OTP is {otp} & {email}")
        return f"otp generated {otp} & {email}"
    else:
        logger.info(f"just Your OTP is {otp} & {email}")
        return f"just otp generated {otp} & {email}"