import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardContent, Typography, Table, TableBody, TableCell, TableHead, TableRow, Paper } from '@mui/material';

const MultiCloudDashboard = () => {
  const [resources, setResources] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/multi-cloud-resources')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch resources');
        }
        return response.json();
      })
      .then(data => {
        setResources(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <Typography>Loading...</Typography>;
  if (error) return <Typography color="error">Error: {error}</Typography>;
  if (!resources) return null;

  const chartData = [
    { name: 'EC2 Instances', count: resources.AWS.EC2_Instances.length },
    { name: 'Lambda Functions', count: resources.AWS.Lambda_Functions.length },
    { name: 'S3 Buckets', count: resources.AWS.S3_Buckets.length },
    { name: 'Resource Groups', count: resources.Azure.ResourceGroups.length },
    { name: 'Virtual Machines', count: resources.Azure.VirtualMachines.length },
  ];

  return (
    <div style={{ padding: '16px' }}>
      <Typography variant="h4" gutterBottom>Multi-Cloud Resources Dashboard</Typography>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
        <Card>
          <CardContent>
            <Typography variant="h6">AWS Resources</Typography>
            <Typography variant="subtitle1">EC2 Instances</Typography>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Instance ID</TableCell>
                  <TableCell>Instance Type</TableCell>
                  <TableCell>State</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {resources.AWS.EC2_Instances.map((instance, index) => (
                  <TableRow key={index}>
                    <TableCell>{instance.InstanceId}</TableCell>
                    <TableCell>{instance.InstanceType}</TableCell>
                    <TableCell>{instance.State}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>

            <Typography variant="subtitle1" style={{ marginTop: '16px' }}>Lambda Functions</Typography>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Function Name</TableCell>
                  <TableCell>Memory Size</TableCell>
                  <TableCell>Runtime</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {resources.AWS.Lambda_Functions.map((func, index) => (
                  <TableRow key={index}>
                    <TableCell>{func.FunctionName}</TableCell>
                    <TableCell>{func.MemorySize}</TableCell>
                    <TableCell>{func.Runtime}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>

            <Typography variant="subtitle1" style={{ marginTop: '16px' }}>S3 Buckets</Typography>
            <ul>
              {resources.AWS.S3_Buckets.map((bucket, index) => (
                <li key={index}>{bucket}</li>
              ))}
            </ul>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography variant="h6">Azure Resources</Typography>
            <Typography variant="subtitle1">Resource Groups</Typography>
            <ul>
              {resources.Azure.ResourceGroups.map((group, index) => (
                <li key={index}>{group}</li>
              ))}
            </ul>

            <Typography variant="subtitle1" style={{ marginTop: '16px' }}>Virtual Machines</Typography>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Location</TableCell>
                  <TableCell>Type</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {resources.Azure.VirtualMachines.map((vm, index) => (
                  <TableRow key={index}>
                    <TableCell>{vm.name}</TableCell>
                    <TableCell>{vm.location}</TableCell>
                    <TableCell>{vm.type}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardContent>
          <Typography variant="h6">Resource Distribution</Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
};

export default MultiCloudDashboard;