#================================================
# dispense.py
#================================================
# Python code for dispensing objects with our
# vending machine

# Legend:
#
# ///-\\\
# |^   ^| 
# |O   O|      ________________ 
# |  ~  |     /  Desperation  /|
#  \ O /     /  Machine 2.0  / |
#   | |     /_______________/  |
#           |       |       |  |
#           |  tl   |  tr   |  |
#           |_______|_______|  |
#           |       |       |  |
#           |  bl   |  br   |  |
#           |_______|_______|  |
#           |  /            |  /
#           | /             | /
#           |/______________|/
#
# Bottom Right (br):
#  - PWM: PIN 16 (GPIO 23)
#  - IN1: PIN 13 (GPIO 27)
#  - IN2: PIN 15 (GPIO 22)
#
# Bottom Left (bl):
#  - PWM: PIN 35 (GPIO 19)
#  - IN1: PIN 37 (GPIO 26)
#  - IN2: PIN 40 (GPIO 21)
#
# Top Right (tr):
#  - PWM: PIN 8  (GPIO 14)
#  - IN1: PIN 10 (GPIO 15)
#  - IN2: PIN 11 (GPIO 17)
#
# Top Left (tl):
#  - PWM: PIN 32 (GPIO 12)
#  - IN1: PIN 36 (GPIO 16)
#  - IN2: PIN 38 (GPIO 20)

import time
import RPi.GPIO as GPIO

# Define pins here

br_pwm = 23
br_in1 = 27
br_in2 = 22

bl_pwm = 19
bl_in1 = 26
bl_in2 = 21

tr_pwm = 14
tr_in1 = 15
tr_in2 = 17

tl_pwm = 12
tl_in1 = 16
tl_in2 = 20

# Define frequency (Hz)

FREQ = 50

def config():
    # Configures our GPIO pins

    # Define overall GPIO as BCM
    GPIO.setmode( GPIO.BCM )

    # Configure all of our GPIO's as outputs
    GPIO.setup( br_pwm , GPIO.OUT )
    GPIO.setup( br_in1 , GPIO.OUT )
    GPIO.setup( br_in2 , GPIO.OUT )

    GPIO.setup( bl_pwm , GPIO.OUT )
    GPIO.setup( bl_in1 , GPIO.OUT )
    GPIO.setup( bl_in2 , GPIO.OUT )

    GPIO.setup( tr_pwm , GPIO.OUT )
    GPIO.setup( tr_in1 , GPIO.OUT )
    GPIO.setup( tr_in2 , GPIO.OUT )

    GPIO.setup( tl_pwm , GPIO.OUT )
    GPIO.setup( tl_in1 , GPIO.OUT )
    GPIO.setup( tl_in2 , GPIO.OUT )

    # Makes sure they're all low to start

    GPIO.output( br_pwm , GPIO.LOW )
    GPIO.output( br_in1 , GPIO.LOW )
    GPIO.output( br_in2 , GPIO.LOW )

    GPIO.output( bl_pwm , GPIO.LOW )
    GPIO.output( bl_in1 , GPIO.LOW )
    GPIO.output( bl_in2 , GPIO.LOW )

    GPIO.output( tr_pwm , GPIO.LOW )
    GPIO.output( tr_in1 , GPIO.LOW )
    GPIO.output( tr_in2 , GPIO.LOW )

    GPIO.output( tl_pwm , GPIO.LOW )
    GPIO.output( tl_in1 , GPIO.LOW )
    GPIO.output( tl_in2 , GPIO.LOW )

def cleanup():
    # Makes sure we're all cleaned up

    # Ensure all PWM pins are stopped

    br_pwm_pin = GPIO.PWM( br_pwm, FREQ )
    bl_pwm_pin = GPIO.PWM( bl_pwm, FREQ )
    tr_pwm_pin = GPIO.PWM( tr_pwm, FREQ )
    tl_pwm_pin = GPIO.PWM( tl_pwm, FREQ )

    br_pwm_pin.stop()
    bl_pwm_pin.stop()
    tr_pwm_pin.stop()
    tl_pwm_pin.stop()

    # Final cleanup
    GPIO.cleanup()

def motor_test():
    # Tests that all of our motors are functional
    # We wait for user response to move on to the
    # next motor

    # Configure the GPIO's
    config()

    # Test br
    GPIO.output( br_in1, GPIO.LOW )
    GPIO.output( br_in2, GPIO.HIGH )

    pwm_pin = GPIO.PWM( br_pwm, FREQ )
    pwm_pin.start( 25 ) # 25% duty cycle
    input( "Testing br..." )

    GPIO.output( br_in1, GPIO.LOW )
    GPIO.output( br_in2, GPIO.LOW )
    pwm_pin.stop()

    # Test bl
    GPIO.output( bl_in1, GPIO.LOW )
    GPIO.output( bl_in2, GPIO.HIGH )

    pwm_pin = GPIO.PWM( bl_pwm, FREQ )
    pwm_pin.start( 25 ) # 25% duty cycle
    input( "Testing bl..." )

    GPIO.output( bl_in1, GPIO.LOW )
    GPIO.output( bl_in2, GPIO.LOW )
    pwm_pin.stop()

    # Test tr
    GPIO.output( tr_in1, GPIO.LOW )
    GPIO.output( tr_in2, GPIO.HIGH )

    pwm_pin = GPIO.PWM( tr_pwm, FREQ )
    pwm_pin.start( 25 ) # 25% duty cycle
    input( "Testing tr..." )

    GPIO.output( tr_in1, GPIO.LOW )
    GPIO.output( tr_in2, GPIO.LOW )
    pwm_pin.stop()

    # Test tl
    GPIO.output( tl_in1, GPIO.LOW )
    GPIO.output( tl_in2, GPIO.HIGH )

    pwm_pin = GPIO.PWM( tl_pwm, FREQ )
    pwm_pin.start( 25 ) # 25% duty cycle
    input( "Testing tl..." )

    GPIO.output( tl_in1, GPIO.LOW )
    GPIO.output( tl_in2, GPIO.LOW )
    pwm_pin.stop()

    # Cleanup at end
    cleanup()

def dispense( location ):
    # Dispenses an iterm from the given location
    #
    # Location is a string, any of:
    #  - "tr"
    #  - "tl"
    #  - "br"
    #  - "bl"
    # (if not, the function does nothing)

    # Configure GPIO's
    config()

    if( location == "tr" ):
        GPIO.output( tr_in1, GPIO.LOW )
        GPIO.output( tr_in2, GPIO.HIGH )

        pwm_pin = GPIO.PWM( tr_pwm, FREQ )
        pwm_pin.start( 25 ) # 25% duty cycle

        time.sleep( 1.9 )

        pwm_pin.stop()
        GPIO.output( tr_in1, GPIO.LOW )
        GPIO.output( tr_in2, GPIO.LOW )

    elif( location == "tl" ):
        GPIO.output( tl_in1, GPIO.LOW )
        GPIO.output( tl_in2, GPIO.HIGH )

        pwm_pin = GPIO.PWM( tl_pwm, FREQ )
        pwm_pin.start( 25 ) # 25% duty cycle

        time.sleep( 1.5 )
        
        pwm_pin.stop()
        GPIO.output( tl_in1, GPIO.LOW )
        GPIO.output( tl_in2, GPIO.LOW )

    elif( location == "br" ):
        GPIO.output( br_in1, GPIO.LOW )
        GPIO.output( br_in2, GPIO.HIGH )

        pwm_pin = GPIO.PWM( br_pwm, FREQ )
        pwm_pin.start( 25 ) # 25% duty cycle

        time.sleep( 1.5 )
        
        pwm_pin.stop()
        GPIO.output( br_in1, GPIO.LOW )
        GPIO.output( br_in2, GPIO.LOW )

    elif( location == "bl" ):
        GPIO.output( bl_in1, GPIO.LOW )
        GPIO.output( bl_in2, GPIO.HIGH )

        pwm_pin = GPIO.PWM( bl_pwm, FREQ )
        pwm_pin.start( 25 ) # 25% duty cycle

        time.sleep( 1.9 )
        
        pwm_pin.stop()
        GPIO.output( bl_in1, GPIO.LOW )
        GPIO.output( bl_in2, GPIO.LOW )

    # Cleanup after
    cleanup()
