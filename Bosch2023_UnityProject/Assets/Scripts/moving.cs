using UnityEngine;
using System.Collections.Generic;
using System.IO;
using TMPro;

public class moving : MonoBehaviour
{
    public string csvFilePath = @"D:\Bosch2023\DataFiles\CSV\normalized_data.csv"; // Path to the CSV file
    private float animationStartTime;
    private int currentRowIndex;
    private List<string[]> csvData; // A list to store CSV data
    private int updateCount = 0;

    [SerializeField] private TMP_Text timeText;
    [SerializeField] private TMP_Text distText;

    [SerializeField] private GameObject target;

    public float speed;
    float dataModifier = 30;
    float dataModifierYaw = 20;

    float currentRotationAngle = 0f; // Initialize the rotation angle
    public float yawRateRadians; // Yaw rate in radians per second.

    private Quaternion initialRotation; // Store the initial rotation of the object

    private void Awake()
    {
        GameObject timeTextObject = GameObject.Find("timeText");
        timeText = timeTextObject.GetComponent<TMP_Text>();

        GameObject distTextObject = GameObject.Find("distText");
        distText = distTextObject.GetComponent<TMP_Text>();
    }

    void Start()
    {
        // Store the initial rotation of the object
        initialRotation = transform.rotation;

        // Check if the CSV file exists
        if (!File.Exists(csvFilePath))
        {
            Debug.LogError("CSV file not found at path: " + csvFilePath);
            return;
        }

        // Read and parse the CSV file
        ReadCSVFile();

        // Start the animation
        animationStartTime = Time.time;
        currentRowIndex = 1; // Start from the second row
    }

    void Update()
    {
        updateCount++;

        if (updateCount % 10 != 0)
        {
            return;
        }

        if (csvData != null && currentRowIndex < csvData.Count)
        {
            float currentTime = Time.time - animationStartTime;

            string timestampString = csvData[currentRowIndex][19];
            // Replace comma with period for parsing
            timestampString = timestampString.Replace('.', ',');

            double timestamp = double.Parse(timestampString);

            //timestamp is 19th col 
            // Find the row in the CSV data that corresponds to the current time
            if (currentRowIndex < csvData.Count - 1 && timestamp > currentTime)
            {
                currentRowIndex++;
            }

            string formattedTimestamp = timestamp.ToString("F3"); // Format to show 3 decimal places
            timeText.text = "Time: " + formattedTimestamp; // Update the text
            distText.text = "Distance x: " + (target.transform.position.x - transform.position.x).ToString("F3") + "\nDistance y: " + (target.transform.position.z - transform.position.z).ToString("F3"); // Update the text

            // Interpolate object positions if there is more than one row of data
            if (currentRowIndex > 1)
            {
                // ROTATION
                // Get the yaw rate from the CSV data (assuming it's in radians per second)
                float yawRateRadians = float.Parse(csvData[currentRowIndex][18].Replace('.', ',')) ;

                // Calculate the rotation angle change based on yaw rate and time
                float rotationAngleChange = yawRateRadians;

                // Calculate the change in position using trigonometry
                float delta_x = speed * Mathf.Sin(currentRotationAngle) * Time.deltaTime;
                float delta_z = speed * Mathf.Cos(currentRotationAngle) * Time.deltaTime;

                delta_x *= dataModifier;
                delta_z *= dataModifier;


                // Update the object's position
                transform.position += new Vector3(delta_x, 0, delta_z);

                // Add the change in rotation angle to the current rotation angle
                currentRotationAngle += rotationAngleChange * Time.deltaTime;



                // Apply the rotation around the Y-axis based on the initial rotation
                transform.rotation = initialRotation * Quaternion.Euler(0, currentRotationAngle * dataModifierYaw * Mathf.Rad2Deg, 0);

                // SPEED
                speed = float.Parse(csvData[currentRowIndex][9].Replace('.', ','));

                Debug.Log(speed + " speed ");
            }
        }
    }

    // Read and parse the CSV file
    private void ReadCSVFile()
    {
        csvData = new List<string[]>();

        using (StreamReader reader = new StreamReader(csvFilePath))
        {
            while (!reader.EndOfStream)
            {
                string line = reader.ReadLine();
                string[] values = line.Split(',');

                // Add the CSV row to the list
                csvData.Add(values);
            }
        }
    }
}
