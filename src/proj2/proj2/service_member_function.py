from tutorial_interfaces.srv import FirstService
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


import rclpy
from rclpy.node import Node
import numpy as np


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')


        self.q1_reference=0.0
        self.q2_reference=0.0
        self.q3_reference=0.0

        self.srv = self.create_service(FirstService, 'input_serv', self.service_callback)
        self.i=0

        self.effort_q1=0.0
        self.effort_q2=0.0
        self.effort_q3=0.0

        
        self.subscription_1 = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
        self.subscription_1



        

        self.publisher_1= self.create_publisher(Float64MultiArray, '/forward_effort_controller/commands', 10)
        msg=Float64MultiArray()
        msg.data=[0.0,0.0,0.0]
        self.publisher_1.publish(msg)
        # timer_period = 0.1  # seconds
        # self.timer = self.create_timer(timer_period, self.publisher_callback)


    def service_callback(self, request, response):
        #response.sum = request.a + request.b
        
        q1=request.x
        q2=request.y
        q3= request.z
        
        response.q1=q1
        response.q2=q2
        response.q3=q3

        self.q1_reference=q1
        self.q2_reference=q2
        self.q3_reference=q3

        return response

    def listener_callback(self,msg):

        # print(msg)

        q1=msg.position[0]
        q2=msg.position[1]
        q3=msg.position[2]

        v1=msg.velocity[0]
        v2=msg.velocity[1]
        v3=msg.velocity[2]

        K_p_q1=9.5
        K_d_q1=7.8

        K_p_q2=5.2
        K_d_q2=6.9

        K_p_q3=100
        K_d_q3=80

        self.effort_q1= -K_p_q1*(q1-self.q1_reference)-K_d_q1*v1
        self.effort_q2=-K_p_q2*(q2-self.q2_reference)-K_d_q2*v2
        self.effort_q3=-K_p_q3*(q3-self.q3_reference)-K_d_q3*v3

        msg=Float64MultiArray()
        msg.data=[float(self.effort_q1),float(self.effort_q2),float(self.effort_q3)]

        self.publisher_1.publish(msg)
        
        if self.i<1000:

            # print(self.i)

            f=open('q1_1.txt','a')
            f.write(str(q1))
            f.write('\n')
            f.close()

            f=open('q2_1.txt','a')
            f.write(str(q2))
            f.write('\n')
            f.close()

            f=open('q3_1.txt','a')
            f.write(str(q3))
            f.write('\n')
            f.close()
        
        self.i+=1


    # def publisher_callback(self):

    #     msg=Float64MultiArray()
    #     msg.data=[float(self.effort_q1),float(self.effort_q2),float(self.effort_q3)]

    #     ##Publish

    #     self.publisher_1.publish(msg)




def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
