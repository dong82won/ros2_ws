# import the empty module from std_servs Service interface
from std_srvs.srv import Empty

# import the ROS2 Python client libraries
import rclpy
from rclpy.node import Node


class ClientAsync(Node):

    def __init__(self):
        # Here you have the class constructor

        # call the class constructor to initialize the node as service_client
        super().__init__('service_client')

        # create the Service Client object
        # defines the name and type of the Service Server you will work with.
        self.client = self.create_client(Empty, 'moving')

        # checks once per second if a Service matching the type and name of the Client is available.
        # 예외처리 반드시 넣어야 한다.
        while not self.client.wait_for_service(timeout_sec=1.0):
            # if it is not available, a message is displayed
            self.get_logger().info('service not available, waiting again...')

        # create an Empty request
        self.req = Empty.Request()

    def send_request(self):

        # send the request
        self.future = self.client.call_async(self.req)
        # 비동기식은 딴 짓을 할 수 있다.


def main(args=None):
    # initialize the ROS communication
    rclpy.init(args=args)

    # declare the node constructor
    client = ClientAsync()

    # run the send_request() method
    client.send_request()

    while rclpy.ok():
        # pause the program execution, waits for a request to kill the node (ctrl+c)
        # 노드를 한번 가동한다.
        rclpy.spin_once(client)

        if client.future.done(): #서비스 동작 완료 여부 확인. 응답 받았어?
            try:
                # checks the future for a response from the Service
                # while the system is running.
                # If the Service has sent a response, the result will be written
                # to a log message.
                # 응답 확인!!
                response = client.future.result()

            except Exception as e:
                # Display the message on the console
                client.get_logger().info('Service call failed %r' % (e,))
            else:
                # Display the message on the console
                client.get_logger().info('the robot is moving' )
            break

        # do somting~~~사용자 코드 작성하면 된다.call_async 비동기라서 가능하다.
        # 여기 추가 제어문을 기재 가능하다. 응답이 없는 상태에서 다른 짓(딴짓) 할 수 있기 때문이다.


    client.destroy_node()
    # shutdown the ROS communication
    rclpy.shutdown()


if __name__ == '__main__':
    main()