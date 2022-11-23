using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class rotateWhenCrash : MonoBehaviour
{

    public float speed = 0.5f;
    public bool moveDown = false;
    public float degreesPerSecond = 45;

    int stepsSinceNoCrash = 0;

    /*

    private void OnCollisionEnter(Collision other){

        stepsSinceNoCrash = 0;

        if(other.collider.tag == "Estante"){
            Debug.Log("heyyy enter");
            bool yourBool= false;
            System.Random rand = new System.Random();

            if (rand.Next(0, 2) != 0)
            {
                yourBool = true;
            } 
            if(yourBool == true) transform.Rotate(new Vector3(0, 0, degreesPerSecond));
            else transform.Rotate(new Vector3(0, 0, -degreesPerSecond));
        }
        
    }
    */

    private void OnCollisionStay(Collision other){

        if(other.collider.tag == "Estante"){
            Debug.Log("heyyy stay");
            bool yourBool= false;
            System.Random rand = new System.Random();

            if (rand.Next(0, 2) != 0)
            {
                yourBool = true;
            } 
            if(yourBool == true) transform.Rotate(new Vector3(0, 0, degreesPerSecond));
            else transform.Rotate(new Vector3(0, 0, -degreesPerSecond));
        }

    }
    private void onCollisionExit(Collider other){
        Debug.Log("UUUUUU");
        if(other.tag == "Estante"){
            Debug.Log("heyyy");
        }
    }

    void Start(){

    }
    void Update(){
        //if(stepsSinceNoCrash > 2000) degreesPerSecond = degreesPerSecond * -1;
        stepsSinceNoCrash ++;
    }
}
