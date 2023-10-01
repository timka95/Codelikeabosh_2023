using UnityEngine;
using System.Collections.Generic;
using System.IO;
using System;

public class visualization : MonoBehaviour
{
    public string csvFilePath = @"D:\Bosch2023\DataFiles\CSV\normalized_data.csv"; // Path to the CSV file
    private float animationStartTime;
    private int currentRowIndex;
    private List<string[]> csvData; // A list to store CSV data

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
        currentRowIndex = 1; // Start from the second row (assuming headers in the first row)
    }

    void Update()
    {
        if (csvData != null && currentRowIndex < csvData.Count)
        {
            float currentTime = Time.time - animationStartTime;

            // Find the row in the CSV data that corresponds to the current time
            while (currentRowIndex < csvData.Count - 1 &&
                   float.Parse(csvData[currentRowIndex][csvData[currentRowIndex].Length - 1]) < currentTime)
            {
                currentRowIndex++;
            }

            // Interpolate object positions if there is more than one row of data
            if (currentRowIndex > 1)
            {
                float previousTime = float.Parse(csvData[currentRowIndex - 1][csvData[currentRowIndex - 1].Length - 1]);
                float deltaTime = currentTime - previousTime;

                // Interpolate object positions based on the timestamps
                Vector3 previousPosition = new Vector3(
                    float.Parse(csvData[currentRowIndex - 1][0]),
                    float.Parse(csvData[currentRowIndex - 1][1]),
                    0f
                );

                Vector3 currentPosition = new Vector3(
                    float.Parse(csvData[currentRowIndex][0]),
                    float.Parse(csvData[currentRowIndex][1]),
                    0f
                );

                float t = deltaTime == 0f ? 0f : (currentTime - previousTime) / deltaTime;

                Vector3 interpolatedPosition = Vector3.Lerp(previousPosition, currentPosition, t);

                // Update the object's position
                transform.position = interpolatedPosition;
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
