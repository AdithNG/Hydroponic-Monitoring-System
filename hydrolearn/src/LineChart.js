import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, registerables, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import 'chartjs-adapter-date-fns';

// Register necessary components from Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ...registerables // Spread registerables directly
);

const LineChart = ({ actualData, predictedData, label, timestamps }) => {
  console.log("Actual Sensor Data: ", actualData);
  console.log("Predicted Data: ", predictedData);
  const chartData = {
    labels: timestamps, // Timestamps for x-axis
    datasets: [
      {
        label: `${label} (Actual)`,
        data: actualData, // Actual data
        fill: false,
        borderColor: 'rgba(75,192,192,1)', // Solid line for actual data
        tension: 0.1,
      },
      {
        label: `${label} (Predicted)`,
        data: predictedData, // Predicted data
        fill: false,
        borderColor: 'rgba(255,99,132,1)', // Different color for predicted data
        borderDash: [5, 5], // Dashed line for predicted data
        tension: 0.1,
      },
    ],
  };

  const options = {
    scales: {
      x: {
        type: 'time', // Use time-based x-axis
        time: {
          unit: 'minute', // Adjust the time unit based on your data
          displayFormats: {
            minute: 'MMM d, h:mm a', // Custom format for the x-axis timestamps
          },
        },
        title: {
          display: true,
          text: 'Timestamps',
        },
      },
      y: {
        title: {
          display: true,
          text: label, // Label for y-axis
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default LineChart;