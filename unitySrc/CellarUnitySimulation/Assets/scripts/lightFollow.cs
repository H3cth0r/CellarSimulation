using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class lightFollow : MonoBehaviour
{

    public GameObject thePlayer;
    public Light lt;


    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        //transform.LookAt(thePlayer.transform);
        Vector3 thePlayerPos = thePlayer.transform.position;
        thePlayerPos.y = 5;
        transform.position = thePlayerPos;
        lt.intensity = Mathf.PingPong(Time.time*2, 3);
    }
}
