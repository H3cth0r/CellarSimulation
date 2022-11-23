using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class moveCharacter : MonoBehaviour
{

    // Speed
    public float speed      =   0.5f;
    public bool  moveDown   =   false;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(moveDown == true){
            this.transform.Translate(Vector3.down * Time.deltaTime * speed);
        } else {
            this.transform.Translate(Vector3.up * Time.deltaTime * speed);
        }
    }
}
