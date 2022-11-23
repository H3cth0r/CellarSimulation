using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class moveRobot : MonoBehaviour
{
    float speed;
    int[] rotY = {0, 90,180, 270};
    int lastRot = 0;
    string last_tag_crash = "";

    Dictionary<string, int> tags_dict = new Dictionary<string, int>(); 

    public int myPriority;
    /*
    public GameObject bb8;
    public GameObject r5;
    public GameObject r2;
    public GameObject android;
    public GameObject robot;
    */

    // Start is called before the first frame update
    void Start()
    {
        speed = Random.Range(0.005f, 0.01f);
        // random range
        tags_dict.Add("bb8_tag", 0);
        tags_dict.Add("r5_tag", 1);
        tags_dict.Add("r2_tag", 2);
        tags_dict.Add("android_tag", 3);
        tags_dict.Add("robot_tag", 4);

    }

    void Move(){
        if(transform.eulerAngles.y == 0){
            transform.position += new Vector3(0, 0, speed);
        }
        else if(transform.eulerAngles.y == 180){
            transform.position += new Vector3(0, 0, -speed);
        }
        else if(transform.eulerAngles.y == 90){
            transform.position += new Vector3(speed, 0, 0);
        }
        else if(transform.eulerAngles.y == 270){
            transform.position += new Vector3(-speed, 0, 0);
        }
    }

    // Update is called once per frame
    void Update()
    {
        Move();
        
    }
    private void OnCollisionStay(Collision Collision){
        int rot = lastRot;
        if( tags_dict.ContainsKey(Collision.collider.tag) && last_tag_crash != Collision.collider.tag){
            if(tags_dict[Collision.collider.tag] > myPriority ){
                if(transform.eulerAngles.y == 0){ 
                    rot = 2;transform.position += new Vector3(0, 0, speed*2);
                }
                else if(transform.eulerAngles.y == 180){
                    rot = 0;transform.position += new Vector3(0, 0, -speed*2);
                }
                else if(transform.eulerAngles.y == 90){
                    rot = 3;transform.position += new Vector3(speed*2, 0, 0);
                }
                else{
                    rot = 1;transform.position += new Vector3(-speed*2, 0, 0);
                }
            }
        }else if(Collision.collider.tag == "Estante" || last_tag_crash == Collision.collider.tag){
            while(true){
                rot = Random.Range(0, rotY.Length);
                if(rotY[rot] != transform.eulerAngles.y){
                    break;
                }
            }
        }
        lastRot = rot;
        last_tag_crash = Collision.collider.tag;
        transform.rotation = Quaternion.Euler(0,rotY[rot], 0);
    }
}
