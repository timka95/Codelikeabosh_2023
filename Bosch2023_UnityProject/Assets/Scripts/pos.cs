using UnityEngine;
using System.Collections.Generic;
using System.IO;

public class pos : MonoBehaviour
{
    public string csvFilePath = @"D:\Bosch2023\DataFiles\vehicle_pos3.csv"; // Path to the CSV file
    public string csvFilePath2 = @"D:\Bosch2023\DataFiles\CSV\normalized_data.csv"; // Path to the CSV file
    private float animationStartTime;
    private int currentRowIndex;
    private List<string[]> csvData; // A list to store CSV data
    private List<string[]> csvData2; // A list to store CSV data
    private int updateCount = 0;

    //[SerializeField] private int carNum;
    [SerializeField] private GameObject mainCar;

    private void Awake()
    {
        mainCar = GameObject.Find("mainCar");
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
        updateCount++;

        if (updateCount % 10 != 0)
        {
            return;
        }


        if (csvData != null && currentRowIndex < csvData.Count)
        {
            float currentTime = Time.time - animationStartTime;


            string timestampString = csvData2[currentRowIndex][19];
            // Replace comma with period for parsing
            timestampString = timestampString.Replace('.', ',');

            double timestamp = double.Parse(timestampString);

            //timestamp is 19th col 
            // Find the row in the CSV data that corresponds to the current time
            if (currentRowIndex < csvData.Count - 1 &&

                   timestamp > currentTime)
            {

                currentRowIndex++;
            }

            //Debug.Log(timestamp);

            // Interpolate object positions if there is more than one row of data
            if (currentRowIndex > 1)
            {

                float previousTime = float.Parse(csvData2[currentRowIndex - 1][19].Replace('.', ','));
                float deltaTime = currentTime - previousTime;

                //Debug.Log(csvData[currentRowIndex - 1][carNum].Replace('.', ',') + " x pos of " + carNum);
                //Debug.Log(csvData[currentRowIndex - 1][carNum+1].Replace('.', ',') + " z pos of " + carNum);

                Debug.Log(csvData[currentRowIndex - 1][0].Replace('.', ','));

                // Interpolate object positions based on the timestamps
                Vector3 previousPosition = new Vector3(
                    float.Parse(csvData[currentRowIndex - 1][0].Replace('.', ',')),
                    0f,
                    float.Parse(csvData[currentRowIndex - 1][1].Replace('.', ','))

                );

                Vector3 currentPosition = new Vector3(
                    float.Parse(csvData[currentRowIndex][0].Replace('.', ',')),
                    0f,
                    float.Parse(csvData[currentRowIndex][1].Replace('.', ','))

                );


                //float adjustedDeltaTime = deltaTime * 0.001f;

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

        csvData2 = new List<string[]>();

        using (StreamReader reader = new StreamReader(csvFilePath2))
        {
            while (!reader.EndOfStream)
            {
                string line = reader.ReadLine();
                string[] values = line.Split(',');

                // Add the CSV row to the list
                csvData2.Add(values);
            }
        }
    }

}
