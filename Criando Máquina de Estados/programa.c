#include <stdio.h>


typedef struct {
    MotorState currentState;
    int cycle_counter;
    int speed_rpm;

} MotorController;

typedef enum{
    IDLE,
    STARTING,
    RUNNING,
    STOPPING,
    ERROR
} MotorState;

typedef enum{
    CMD_START,
    CMD_STOP,
    CMD_RESET
} MotorCommand;

void motor_init(MotorController* motor){
    motor->currentState = IDLE;
    motor->cycle_counter = 0;
    motor->speed_rpm = 0;
}

void char* get_state_name(MotorState state){

    switch(state){
        case 
    }

}

int main(){
    
    return 0;
}