// publisher_member_function.cpp (여러 노드 생성)
// 멀티스레딩 사용
// 멀티스레드를 사용하여 두 노드를 동시에 실행할 수 있습니다.
// 이를 위해 std::thread를 활용합니다.

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

#include <sstream>
#include <thread>

class Talker : public rclcpp::Node
{
public:
    Talker() : Node("talker_count"), count_(0)
    {
        publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
        timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&Talker::publish_message, this));
    }

private:
    void publish_message()
    {
        auto msg = std_msgs::msg::String();
        msg.data = std::string("Hello from ") + this->get_name() + std::to_string(count_++);
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
        publisher_->publish(msg);
    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;

    int count_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);

    // 여러 노드 생성
    auto talker_only = std::make_shared<Talker>();
    rclcpp::spin(talker_only);

    rclcpp::shutdown();
    return 0;
}
