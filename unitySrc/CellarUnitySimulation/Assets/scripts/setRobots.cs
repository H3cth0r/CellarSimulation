using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class setRobots : MonoBehaviour
{
    public GameObject[] Robots;
    Vector3[] poses = {new Vector3(-55.2f, -4.23f, 2f),         new Vector3(-42.4f, -4.23f, 0.1f),     new Vector3(-12.1f, -4.23f, -11.6f),
                           new Vector3(-40.5f, -4.23f, -11.6f), new Vector3(-54.5f, -4.23f, -11.67f),   new Vector3(-12.1f, -4.2f, -17.9f),
                           new Vector3(-14.2f, -4.2f, -12.6f),  new Vector3(12.9f, -4.23f, 12.6f),      new Vector3(12.9f, -4.2f, 0.6f),
                           new Vector3(16f, -4.2f, -8f),        new Vector3(14.5f, -4.2f, -23.4f),      new Vector3(2f, -4.2f, -23.4f),
                           new Vector3(-7.2f, -4.2f, -23.4f),   new Vector3(-7.2f, -4.2f, -19.4f),      new Vector3(-25.3f, -4.2f, -12.3f)};
                    

    // Start is called before the first frame update
    void Start()
    {
        List<Vector3> array_pos = new List<Vector3>();
        for(int i = 0; i < poses.Length; i ++){
            array_pos.Add(poses[i]);
        }
        System.Random rnd = new System.Random();
        for(int i = 0; i < Robots.Length; i++){
            int randomIndex = rnd.Next(0, array_pos.Count);
            Robots[i].transform.position = array_pos[randomIndex];
            array_pos.RemoveAt(randomIndex);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
