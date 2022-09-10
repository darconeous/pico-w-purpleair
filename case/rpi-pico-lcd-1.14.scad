
// base is 28mm x 17mm


board_w=25.5;
board_l=53;
board_t=2.1;
pack_d=17;
wall_w=2;
notch_depth=0.6;
cavity_w=board_w-notch_depth*2;
base_w=cavity_w+wall_w*2;
base_d=pack_d+wall_w*2;
usb_conn_depth=17;

module outer_case() {
    cube([base_w,base_d,wall_w+board_l]);
}

module wall_lid() {
    cube([base_w,base_d,wall_w]);
}

module inner_case()
{
    translate([wall_w,wall_w,wall_w])cube([cavity_w,pack_d+4,board_l+1]);
    #translate([wall_w-(board_w-cavity_w)/2,pack_d+wall_w-1,wall_w-notch_depth])cube([board_w,board_t,board_l+5]);
    #translate([wall_w+(cavity_w)/2,wall_w+2.5+pack_d-usb_conn_depth,-1])cube([10,5,10],center=true);
}

module angle_stand() {
    $fs=1;
    round_rad=5;
    tilt_angle=45;
    difference() {
        hull(){
            rotate([0,0,-tilt_angle])
            outer_case();
            translate([round_rad,-base_w*0.65])cylinder(wall_w+board_l,r=round_rad);
            translate([round_rad,base_w*0.4])cylinder(wall_w+board_l,r=round_rad);
        }
        rotate([0,0,-tilt_angle])
        inner_case();
    }
}

module wall_stand() {
    difference() {
        hull(){
            outer_case();
        }
        inner_case();
    }
}

translate([15,0,0])angle_stand();

//translate([15,15,0])rotate([0,0,-90])wall_lid();
//translate([13,-15,0])rotate([0,0,90])wall_stand();