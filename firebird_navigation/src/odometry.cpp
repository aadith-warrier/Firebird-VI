#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "geometry_msgs/msg/transform_stamped.hpp"

using namespace std::chrono_literals;
using std::placeholders::_1;

class OdometryPublisher : public rclcpp::Node
{
    public:
        OdometryPublisher()
        : Node("odometry_publisher")
        {
            subscription = this->create_subscription<nav_msgs::msg::Odometry>("/odom", 10, std::bind(&OdometryPublisher::publish_odometry_transform, this, _1));
            odometry_transform_broadcaster=std::make_unique<tf2_ros::TransformBroadcaster>(*this);
        }

    private:

    void publish_odometry_transform(const nav_msgs::msg::Odometry::SharedPtr msg)
    {
        geometry_msgs::msg::TransformStamped t;
        t.header.stamp = this->get_clock()->now();
        t.header.frame_id = "odom";
        t.child_frame_id = "base_link";
        t.transform.translation.x = msg->pose.pose.position.x;
        t.transform.translation.y = msg->pose.pose.position.y;
        t.transform.translation.z = msg->pose.pose.position.z;
        t.transform.rotation.x = msg->pose.pose.orientation.x;
        t.transform.rotation.y = msg->pose.pose.orientation.y;
        t.transform.rotation.z = msg->pose.pose.orientation.z;
        t.transform.rotation.w = msg->pose.pose.orientation.w;

        odometry_transform_broadcaster->sendTransform(t);
    }
    
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr subscription;
    std::unique_ptr<tf2_ros::TransformBroadcaster> odometry_transform_broadcaster;

};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    std::cout << "Publishing Odometry Transform!!!" << std::endl;
    rclcpp::spin(std::make_shared<OdometryPublisher>());
    rclcpp::shutdown();
}
