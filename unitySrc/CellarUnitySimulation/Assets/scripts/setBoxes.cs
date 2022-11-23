using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class setBoxes : MonoBehaviour
{
    Vector3[] poses = {     new Vector3(-38.19f, -4.38f, -18.57f),  new Vector3(-25f, -4.4f, -23.4f),       new Vector3(-8.31f, -4.38f, -14.74f),
                            new Vector3(-25.3f, -4.2f, -12.3f),     new Vector3(-22.89f, -4.38f, 2.03f),    new Vector3(-4.7f, -4.4f, 6.6f),
                            new Vector3(-35.4f, -4.4f, 14f),        new Vector3(14f, -4.4f, -15.6f),        new Vector3(14f, -4.4f, -6f),
                            new Vector3(11.4f, -4.4f, -0.2f),       new Vector3(-35.2f, -4.4f, -9.1f),      new Vector3(-22.1f, -4.4f, 12.7f),
                            new Vector3(-60.5f, -4.4f, -17f),       new Vector3(-60.5f, -4.4f, -9.5f),      new Vector3(-55.1f, -4.4f, 2.4f)};
                
    public GameObject[] Boxes;
    
    // Start is called before the first frame update
    void Start()
    {
        List<Vector3> array_pos = new List<Vector3>();
        for(int i = 0; i < poses.Length; i ++){
            array_pos.Add(poses[i]);
        }
        System.Random rnd = new System.Random();
        for(int i = 0; i < Boxes.Length; i++){
            int randomIndex = rnd.Next(0, array_pos.Count);
            Boxes[i].transform.position = array_pos[randomIndex];
            array_pos.RemoveAt(randomIndex);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
