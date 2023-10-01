using UnityEngine;
using System.Collections.Generic;
using System.IO;
using TMPro;

public class movingTimka : MonoBehaviour
{
    public string csvFilePath = @"D:\Bosch2023\DataFiles\CSV\normalized_data.csv"; // Path to the CSV file
    private float animationStartTime;
    private int currentRowIndex;
    private List<string[]> csvData; // A list to store CSV data

    [SerializeField] private TMP_Text timeText;
    [SerializeField] private GameObject[] objectsToMove;
    [SerializeField] private GameObject vehicle;

    private float[] x;
    private float[] y;
    private float[] theta;
    private float[] speed;
    private float[] yawRate;
    private double[] timestamps;

    private const int numObjects = 4;

    void Awake()
    {
        vehicle = gameObject;

        GameObject timeTextObject = GameObject.Find("timeText");
        timeText = timeTextObject.GetComponent<TMP_Text>();

        // Initialize arrays
        x = new float[objectsToMove.Length];
        y = new float[objectsToMove.Length];
        theta = new float[objectsToMove.Length];
        speed = new float[objectsToMove.Length];
        yawRate = new float[objectsToMove.Length];
        timestamps = new double[objectsToMove.Length];
    }

    void Start()
    {
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
        if (csvData != null && currentRowIndex < csvData.Count)
        {
            float currentTime = Time.time - animationStartTime;

            string timestampString = csvData[currentRowIndex][19];
            timestampString = timestampString.Replace('.', ',');
            double timestamp = double.Parse(timestampString);

            if (currentRowIndex < csvData.Count - 1 && timestamp > currentTime)
            {
                currentRowIndex++;
            }

            string formattedTimestamp = timestamp.ToString("F3");
            timeText.text = "Time: " + formattedTimestamp;

            if (currentRowIndex > 0)
            {
                for (int i = 0; i < 1; i++)
                {
                    yawRate[i] = float.Parse(csvData[currentRowIndex][18].Replace('.', ','));
                    float rotationAngleChange = yawRate[i] * Mathf.Rad2Deg * Time.deltaTime;
                    theta[i] += rotationAngleChange;

                    Vector3 positionChange = new Vector3(speed[i] * Mathf.Cos(theta[i]) * Time.deltaTime,
                                                        0,
                                                        speed[i] * Mathf.Sin(theta[i]) * Time.deltaTime);
                    Vector3 newPosition = objectsToMove[i].transform.position + positionChange;

                    objectsToMove[i].transform.position = newPosition;
                    objectsToMove[i].transform.rotation = Quaternion.Euler(0, theta[i] * Mathf.Rad2Deg, 0);
                }

                // Update the vehicle
                float vehicleRotationAngleChange = yawRate[0] * Mathf.Rad2Deg * Time.deltaTime;
                theta[0] += vehicleRotationAngleChange;

                Vector3 vehiclePositionChange = new Vector3(speed[0] * Mathf.Cos(theta[0]) * Time.deltaTime,
                                                            0,
                                                            speed[0] * Mathf.Sin(theta[0]) * Time.deltaTime);
                Vector3 newVehiclePosition = vehicle.transform.position + vehiclePositionChange;

                vehicle.transform.position = newVehiclePosition;
                vehicle.transform.rotation = Quaternion.Euler(0, theta[0] * Mathf.Rad2Deg, 0);
            }
        }
    }

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
