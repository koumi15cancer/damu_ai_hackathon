import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  Card,
  Chip,
  CircularProgress,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Alert,
  SelectChangeEvent,
} from "@mui/material";
import {
  Psychology,
  Science,
  Analytics,
  Refresh,
  CheckCircle,
  Settings,
} from "@mui/icons-material";
import axios from "axios";

interface AIProvider {
  name: string;
  models: string[];
  description: string;
}

interface AIProvidersInfo {
  available_providers: string[];
  current_provider: string;
  providers_info: {
    [key: string]: AIProvider;
  };
}

interface AITestConfig {
  test_name: string;
  providers: string[];
  traffic_split?: { [key: string]: number };
}

interface AITestResult {
  test_name: string;
  providers: string[];
  results: {
    [key: string]: {
      success_rate: number;
      avg_response_time: number;
      total_requests: number;
    };
  };
}

interface AIPerformanceStats {
  total_requests: number;
  success_rate: number;
  avg_response_time: number;
  error_rate: number;
  provider_breakdown: {
    [key: string]: {
      requests: number;
      success_rate: number;
      avg_response_time: number;
    };
  };
}

interface AIManagementProps {
  onProviderChange?: (provider: string) => void;
}

const AIManagement: React.FC<AIManagementProps> = ({ onProviderChange }) => {
  const [aiProviders, setAiProviders] = useState<AIProvidersInfo | null>(null);
  const [aiPerformance, setAiPerformance] = useState<AIPerformanceStats | null>(
    null
  );
  const [abTestConfig, setAbTestConfig] = useState<AITestConfig>({
    test_name: "",
    providers: [],
  });
  const [abTestResults, setAbTestResults] = useState<AITestResult | null>(null);
  const [abTestActive, setAbTestActive] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    loadAIProviders();
    loadAIPerformance();
  }, []);

  const loadAIProviders = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/api/ai/providers"
      );
      setAiProviders(response.data);
    } catch (error) {
      console.error("Failed to load AI providers:", error);
    }
  };

  const loadAIPerformance = async () => {
    try {
      const response = await axios.get(
        "http://localhost:5000/api/ai/performance"
      );
      setAiPerformance(response.data.performance_stats);
    } catch (error) {
      console.error("Failed to load AI performance:", error);
    }
  };

  const handleSwitchAIProvider = async (provider: string) => {
    try {
      const response = await axios.post(
        "http://localhost:5000/api/ai/switch-provider",
        {
          provider: provider,
        }
      );

      if (response.data.message) {
        await loadAIProviders();
        setError("");
        if (onProviderChange) {
          onProviderChange(provider);
        }
      }
    } catch (error) {
      console.error("Failed to switch AI provider:", error);
      setError("Failed to switch AI provider");
    }
  };

  const handleSetupABTest = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5000/api/ai/ab-test/setup",
        abTestConfig
      );

      if (response.data.message) {
        setAbTestActive(true);
        setError("");
        setAbTestConfig({
          test_name: "",
          providers: [],
        });
      }
    } catch (error) {
      console.error("Failed to setup A/B test:", error);
      setError("Failed to setup A/B test");
    }
  };

  const handleGetABTestResults = async () => {
    try {
      const response = await axios.get(
        `http://localhost:5000/api/ai/ab-test/results/${abTestConfig.test_name}`
      );
      setAbTestResults(response.data);
    } catch (error) {
      console.error("Failed to get A/B test results:", error);
      setError("Failed to get A/B test results");
    }
  };

  return (
    <Box>
      <Typography variant='h4' gutterBottom sx={{ color: "#2c3e50", mb: 3 }}>
        🤖 AI Management
      </Typography>

      {/* Error Display */}
      {error && (
        <Alert severity='error' sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* AI Providers */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant='h6' gutterBottom sx={{ mb: 2 }}>
          <Psychology sx={{ mr: 1, verticalAlign: "middle" }} />
          AI Providers
        </Typography>

        {aiProviders ? (
          <Grid container spacing={2}>
            {aiProviders.available_providers.map((provider) => (
              <Grid item xs={12} md={4} key={provider}>
                <Card
                  sx={{
                    p: 2,
                    border: aiProviders.current_provider === provider ? 2 : 1,
                    borderColor:
                      aiProviders.current_provider === provider
                        ? "#3498db"
                        : "#e0e0e0",
                    backgroundColor:
                      aiProviders.current_provider === provider
                        ? "#f8f9fa"
                        : "white",
                  }}>
                  <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                    <Typography variant='h6' sx={{ fontWeight: "bold" }}>
                      {aiProviders.providers_info[provider]?.name || provider}
                    </Typography>
                    {aiProviders.current_provider === provider && (
                      <CheckCircle sx={{ ml: 1, color: "#27ae60" }} />
                    )}
                  </Box>

                  <Typography variant='body2' sx={{ color: "#7f8c8d", mb: 2 }}>
                    {aiProviders.providers_info[provider]?.description ||
                      "AI provider"}
                  </Typography>

                  <Box sx={{ mb: 2 }}>
                    <Typography variant='caption' sx={{ fontWeight: "bold" }}>
                      Available Models:
                    </Typography>
                    <Box
                      sx={{
                        display: "flex",
                        flexWrap: "wrap",
                        gap: 0.5,
                        mt: 0.5,
                      }}>
                      {aiProviders.providers_info[provider]?.models
                        .slice(0, 3)
                        .map((model) => (
                          <Chip
                            key={model}
                            label={model}
                            size='small'
                            variant='outlined'
                          />
                        ))}
                    </Box>
                  </Box>

                  <Button
                    variant={
                      aiProviders.current_provider === provider
                        ? "outlined"
                        : "contained"
                    }
                    size='small'
                    onClick={() => handleSwitchAIProvider(provider)}
                    disabled={aiProviders.current_provider === provider}
                    fullWidth>
                    {aiProviders.current_provider === provider
                      ? "Current"
                      : "Switch to"}
                  </Button>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : (
          <CircularProgress />
        )}
      </Paper>

      {/* A/B Testing */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant='h6' gutterBottom sx={{ mb: 2 }}>
          <Science sx={{ mr: 1, verticalAlign: "middle" }} />
          A/B Testing
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label='Test Name'
              value={abTestConfig.test_name}
              onChange={(e) =>
                setAbTestConfig((prev) => ({
                  ...prev,
                  test_name: e.target.value,
                }))
              }
              placeholder='e.g., team-bonding-test-1'
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Select Providers</InputLabel>
              <Select
                multiple
                value={abTestConfig.providers}
                onChange={(e: SelectChangeEvent<string[]>) =>
                  setAbTestConfig((prev) => ({
                    ...prev,
                    providers:
                      typeof e.target.value === "string"
                        ? [e.target.value]
                        : e.target.value,
                  }))
                }
                renderValue={(selected) => (
                  <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} size='small' />
                    ))}
                  </Box>
                )}>
                {aiProviders?.available_providers.map((provider) => (
                  <MenuItem key={provider} value={provider}>
                    {provider}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
              <Button
                variant='contained'
                onClick={handleSetupABTest}
                disabled={
                  !abTestConfig.test_name || abTestConfig.providers.length < 2
                }>
                Setup A/B Test
              </Button>

              {abTestActive && (
                <Chip
                  icon={<CheckCircle />}
                  label='A/B Test Active'
                  color='success'
                />
              )}

              {abTestActive && abTestConfig.test_name && (
                <Button variant='outlined' onClick={handleGetABTestResults}>
                  Get Results
                </Button>
              )}
            </Box>
          </Grid>
        </Grid>

        {/* A/B Test Results */}
        {abTestResults && (
          <Box sx={{ mt: 3 }}>
            <Typography variant='h6' gutterBottom>
              A/B Test Results: {abTestResults.test_name}
            </Typography>
            <TableContainer>
              <Table size='small'>
                <TableHead>
                  <TableRow>
                    <TableCell>Provider</TableCell>
                    <TableCell>Success Rate</TableCell>
                    <TableCell>Avg Response Time</TableCell>
                    <TableCell>Total Requests</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {abTestResults.providers.map((provider) => (
                    <TableRow key={provider}>
                      <TableCell>{provider}</TableCell>
                      <TableCell>
                        {(
                          (abTestResults.results[provider]?.success_rate ?? 0) *
                          100
                        ).toFixed(1)}
                        %
                      </TableCell>
                      <TableCell>
                        {(
                          abTestResults.results[provider]?.avg_response_time ??
                          0
                        ).toFixed(2)}
                        s
                      </TableCell>
                      <TableCell>
                        {abTestResults.results[provider]?.total_requests ?? 0}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}
      </Paper>

      {/* AI Performance */}
      <Paper sx={{ p: 3 }}>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            mb: 2,
          }}>
          <Typography variant='h6'>
            <Analytics sx={{ mr: 1, verticalAlign: "middle" }} />
            AI Performance
          </Typography>
          <IconButton onClick={loadAIPerformance}>
            <Refresh />
          </IconButton>
        </Box>

        {aiPerformance ? (
          <Grid container spacing={3}>
            <Grid item xs={12} md={3}>
              <Card sx={{ p: 2, textAlign: "center" }}>
                <Typography
                  variant='h4'
                  sx={{ color: "#3498db", fontWeight: "bold" }}>
                  {aiPerformance.total_requests}
                </Typography>
                <Typography variant='body2' sx={{ color: "#7f8c8d" }}>
                  Total Requests
                </Typography>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card sx={{ p: 2, textAlign: "center" }}>
                <Typography
                  variant='h4'
                  sx={{ color: "#27ae60", fontWeight: "bold" }}>
                  {(aiPerformance.success_rate * 100).toFixed(1)}%
                </Typography>
                <Typography variant='body2' sx={{ color: "#7f8c8d" }}>
                  Success Rate
                </Typography>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card sx={{ p: 2, textAlign: "center" }}>
                <Typography
                  variant='h4'
                  sx={{ color: "#f39c12", fontWeight: "bold" }}>
                  {(aiPerformance.avg_response_time ?? 0).toFixed(2)}s
                </Typography>
                <Typography variant='body2' sx={{ color: "#7f8c8d" }}>
                  Avg Response Time
                </Typography>
              </Card>
            </Grid>

            <Grid item xs={12} md={3}>
              <Card sx={{ p: 2, textAlign: "center" }}>
                <Typography
                  variant='h4'
                  sx={{ color: "#e74c3c", fontWeight: "bold" }}>
                  {(aiPerformance.error_rate * 100).toFixed(1)}%
                </Typography>
                <Typography variant='body2' sx={{ color: "#7f8c8d" }}>
                  Error Rate
                </Typography>
              </Card>
            </Grid>
          </Grid>
        ) : (
          <CircularProgress />
        )}
      </Paper>
    </Box>
  );
};

export default AIManagement;
