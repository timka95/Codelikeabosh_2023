using UnityEngine;

public class FollowCar : MonoBehaviour
{
    [SerializeField] private GameObject mainCar; // Reference to the main car GameObject

    public Vector3 offset = new Vector3(0, 130, 0); // Offset from the car's position

    void Start()
    {
        // Find the main car GameObject by its tag, assuming it has the tag "MainCar"
        //mainCar = GameObject.FindGameObjectWithTag("mainCar");

        if (mainCar == null)
        {
            Debug.LogError("Main car not found. Make sure it has the tag 'MainCar'.");
        }
    }

    void FixedUpdate()
    {
        if (mainCar != null)
        {
            //Debug.Log("QDFSGSDFGSDF");



            // Set the camera's position to match the main car's position with the offset
            transform.position = mainCar.transform.position + offset;

            //// Make the camera look at the main car's position
            //transform.LookAt(mainCar.transform.position);
        }
    }
}
