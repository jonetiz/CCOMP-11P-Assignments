# Model Indi Assignment Template
# written by Joe Manlove
# last revision 5/31/20
# the assingment is to comment this, ergo there are no comments past this

# Import choice from random module
from random import choice

# Define global object containers
locations = []
humans = []
dogs = []

# Return a string representation of a given list of balls
def ball_string(balls: list[str]):
    if len(balls) == 0:
        # If there are no balls, user has no balls
        return 'no balls'
    elif len(balls) == 1:
        # Return the ball
        return f'{balls[0].name}'
    elif len(balls) == 2:
        # Return ball[0] and ball[1]
        return f'{balls[0].name} and {balls[1].name}'
    else:
        # If there are more than 3 balls
        return_string = ''
        for ball in balls[:-1]:
            # Append "ball.name," to the return_string for all balls except the last one
            return_string += ball.name + ', '
        # Append "and ball.name" to return_string for the last ball
        return_string += f'and {balls[-1].name}'
        # Return return_string
        return return_string

# Class definitions
class Human:
    def __init__(self, name):
        # Initialize balls as an empty list
        self.balls = []
        # Initialize name as passed name
        self.name = name

    def action(self):
        # If Human has any balls, prompt them to throw the ball
        if self.balls != []:
            # List the balls the Human has
            print(f'\nYou now have {ball_string(self.balls)} in your hands...')
            action = input('Throw the ball?\n')
            if action.lower() in ['yes', 'y']:
                # If user responds with 'yes', or 'y', throw a random ball at a random location
                self.throw_ball(choice(self.balls), choice(locations))
            else:
                # If the user doesn't explicitly say 'yes' or 'y' to throw the ball, they are inherently evil
                print('You really are heartless aren\'t you?')

    def throw_ball(self, ball, target_location):
        # Append the thrown ball to the target_location's balls
        target_location.balls.append(ball)
        # Remove the ball from the Human's balls
        self.balls.remove(ball)
        # Print that ball is thrown to the target
        print(
            f'You have thrown {ball.name}, it is now in the {target_location.name}.\n'
        )

# Ball class with attirbute name
class Ball:
    def __init__(self, name):
        self.name = name


# Location class with attributes name and balls
class Location:
    def __init__(self, name, balls: list[Ball]):
        self.name = name
        self.balls = balls


# Dog class with attributes name and balls
class Dog:
    def __init__(self, name):
        # Initialize name as passed name variable
        self.name = name
        # Initialize balls as an empty list
        self.balls = []

    def action(self):
        # If the dog has a ball
        if self.balls != []:
            # Give a random held ball to a random human
            self.give_ball(choice(humans), choice(self.balls))
        else:
            # Else look for a ball in a random location
            self.look_for_ball(choice(locations))

    def give_ball(self, human, ball):
        # Give the passed Ball to the passed Human
        # Remove the passed Ball from self.balls
        self.balls.remove(ball)
        # Append the passed Ball to Human balls
        human.balls.append(ball)
        # Print that this dog gave the passed Ball to the passed Human
        print(f'{self.name} has given the {ball.name} to {human.name}')

    # Returns a random ball at the targetLocation which will be acted upon in the next iteration of action()
    def look_for_ball(self, target_location):
        # If the targetLocation has any balls
        if target_location.balls != []:
            # Get a random Ball from Location.balls
            target_ball = choice(target_location.balls)
            # Append the chosen Ball to self.balls
            self.balls.append(target_ball)
            # Remove the chosen Ball from Location.balls
            target_location.balls.remove(target_ball)
            # Print that Dog found Ball in Location
            print(
                f'{self.name} has found the {target_ball.name} in the {target_location.name}.'
            )
        else:
            # If there is no Ball, print that Dog finds nothing in the target_location
            print(
                f'{self.name} looks hopelessly about after searching the {target_location.name}.'
            )

# Initialize locations as a list of type Location
locations = [
    Location('Living Room', [Ball('Pink Torus')]),
    Location(
        'Kitchen',
        [Ball('Sal the Snake'),
         Ball('Pink Ellipsoid'),
         Ball('Blue Chuckit')]),
    Location('Under the Couch',
             [Ball('Pink Ball'),
              Ball('Green Ellipsoid'),
              Ball('Blue Torus')]),
    Location('Dining Room', []),
    Location(
        'Yard',
        [Ball('Larry the Lizard'), Ball('S toy')])
]
# Create a Human object with name Joe
joe = Human('Joe')
# Append joe to the humans array
humans.append(joe)
# Create a Dog object with name Indi
indi = Dog('Indi')
# Append indi to the dogs array
dogs.append(indi)

# Main function
def main():
    while True:
        # Indfeinitely process indi and joe action
        indi.action()
        joe.action()

# PEP 299; prevent this code from running if it's imported as a module (as if that'll ever happen)
if __name__ == "__main__":
    main()