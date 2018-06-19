import sys

from Geometry import angles,AngularSpeed, GeometryUtil,Polar,TransformationMatrix,Vector2,Vector3
from PerceptorParsing import switch_case
import io,math

class AccelerometerState:

    def __init__(self, label, acceleration_vector):
        self.label = label
        self.acceleration_vector = acceleration_vector

    def __str__(self):
        return str(self.label)+ " " + str(self.acceleration_vector)

class FieldSide:
    unkwonn = 0
    left = 1 
    right = 2

class ForceState:

    def __init__(self, label, point_on_body, force_vector):
        self.label = label
        self.point_on_body = point_on_body
        self.force_vector = force_vector
    
    def __str__(self):
        return "Point =" + str(self.point_on_body)+ ", Force =" + str(self.force_vector)

class GyroState:

    def __init__(self, label, x_orientation, y_orientation, z_orientation):
        self.label = label
        self.x_orientation = x_orientation
        self.y_orientation = y_orientation
        self.z_orientation = z_orientation
    
    def __str__(self):
        return str(label) + " X=" + self.x_orientation + " Y=" + self.y_orientation + " Z=" +self.z_orientation
    
class HeardMessage:

    def __init__(self,time,direction, message):
        if not message:
            raise(BaseException)
        else:
            self.heard_at_time = time
            self.relative_direction = direction
            self.text = message.text
    
    def is_from_self(self):
        return self.relative_direction.is_nan
    
    def __str__(self):
        return "Message " + "'" +str(self.text) + "'" + " at " + str(self.heard_at_time) + ' from ' + str(self.relative_direction)

class Landmark:
    flag_left_top = 0
    flag_left_bottom = 1
    flag_right_top = 2
    flag_right_bottom = 3
    goal_left_top = 4
    goal_left_bottom = 5
    goal_right_top = 6
    goal_right_bottom = 7

class LandmarkPosition:
    def __init__(self, landmark, radial_position):
        self.landmark = landmark
        self.polar_position = radial_position

class PerceptorState:

    def __init__(self, simulation_time, game_time, play_mode, team_side, player_id, gyro_rates, hinge_joint_states, universal_joint_states,
    touch_states, force_states, accelerometer_states, landmark_positions, visible_lines, team_mate_positions, opposition_positions, ball_position, agent_battery, agent_temperature,
    heard_messages, agent_position):

        self.simulation_time = simulation_time
        self.game_time = game_time
        self.play_mode = play_mode
        self.team_side = team_side
        self.uniform_number = player_id
        self.gyro_states = gyro_rates
        self.hinge_states = hinge_joint_states
        self.universal_joint_states = universal_joint_states
        self.touch_states = touch_states
        self.force_states = force_states
        self.accelerometer_states = accelerometer_states
        self.landmark_positions = landmark_positions
        self.visible_lines = visible_lines
        self.team_mate_positions = team_mate_positions
        self.opposition_positions = opposition_positions
        self.ball_position = ball_position
        self.agent_battery = agent_battery
        self.agent_temperature = agent_temperature
        self.heard_messages = heard_messages
        self.agent_position = agent_position
    
    def try_get_hinge_angle(self, hinge):
        if not self.hinge_states:
            for hj in self.hinge_states:
                if hj.label == hinge.perceptor_label:
                    angle = hj.angle
                    return angle
        angle = angles.Angle(math.nan)
        return False

    def __str__(self):
        sb = str()
        sb += "Simulation_time = " + str(self.simulation_time)
        sb += "\nGame_time = " + str(self.game_time)
        sb += "\nPlay_mode = " + str(self.play_mode)

        if self.agent_battery.has_value:
            sb += "\n Agent_battery = " + str(self.agent_battery)
        
        if self.agent_temperature.has_value:
            sb += "\n Agent_temperature = " + str(self.agent_temperature)
        
        if self.hinge_states:
            for j in self.hinge_states:
                sb += "\nHinge Joint '"+ str(j.label)+ "' -> " + str(j.angle.degrees)

        if self.universal_joint_states:
            for j in self.universal_joint_states:
                sb += "\nAccelerometer '"+ str(j.label)+ "' -> " + str(j.acceleration_vector)
        
        if self.gyro_states:
            for j in self.gyro_states:
                sb += "\nGyro '"+ str(j.label)+ "' -> " + str(j.x_orientation) + ', ' + str(j.y_orientation) + ', ' + str(j.z_orientation)

        if self.touch_states:
            for j in self.touch_states:
                sb += "\nTouch State '" + str(j.label) + "' -> " + str(j.is_touching)

        if self.force_states:
            for j in self.force_states:
                sb += "\nForce State '" + str(j.label) + "' -> pos " + str(j.point_on_body) + ", force " + str(j.force_vector)
        
        