import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  Container,
  Paper,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  FormGroup,
  Grid,
  Divider,
  Rating,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  SelectChangeEvent,
  Tabs,
  Tab,
  IconButton,
} from "@mui/material";
import {
  ExpandMore,
  LocationOn,
  AttachMoney,
  Group,
  Star,
  Restaurant,
  LocalBar,
  SportsEsports,
  Nature,
  EmojiEvents,
  Schedule,
  Directions,
  Psychology,
  Science,
  Settings,
} from "@mui/icons-material";
import axios from "axios";
import AIManagement from "./AIManagement";
import TeamMemberManagement from "./TeamMemberManagement";

interface TeamMember {
  id: string;
  name: string;
  location: string;
  preferences: string[];
  vibe: string;
}

interface EventPhase {
  activity: string;
  location: string;
  map_link: string;
  cost: number;
  indicators: string[];
}

interface EventPlan {
  phases: EventPhase[];
  total_cost: number;
  contribution_needed: number;
  fit_analysis: string;
  rating: number;
}

interface UserPreferences {
  theme: string;
  budget_contribution: string;
  available_members: string[];
  date_time?: string;
  location_zone?: string;
}

function App() {
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [plans, setPlans] = useState<EventPlan[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [selectedPlan, setSelectedPlan] = useState<EventPlan | null>(null);
  const [planDialogOpen, setPlanDialogOpen] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<number>(0);

  const [userPreferences, setUserPreferences] = useState<UserPreferences>({
    theme: "fun 🎉",
    budget_contribution: "No",
    available_members: [],
    date_time: "",
    location_zone: "",
  });

  // Load team members on component mount
  useEffect(() => {
    loadTeamMembers();
  }, []);

  const loadTeamMembers = async () => {
    try {
      const response = await axios.get("http://localhost:5000/team-members");
      setTeamMembers(response.data);
      // Set all members as available by default
      setUserPreferences((prev: UserPreferences) => ({
        ...prev,
        available_members: response.data.map(
          (member: TeamMember) => member.name
        ),
      }));
    } catch (error) {
      console.error("Failed to load team members:", error);
      setError(
        "Failed to load team members. Please check if the backend server is running."
      );
    }
  };

  const handleGeneratePlans = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        "http://localhost:5000/generate-plans",
        userPreferences
      );

      if (response.data.error) {
        setError(response.data.error);
        return;
      }

      setPlans(response.data);
    } catch (error) {
      console.error("Failed to generate plans:", error);
      setError("Failed to generate team bonding plans. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleMemberToggle = (memberName: string) => {
    setUserPreferences((prev: UserPreferences) => ({
      ...prev,
      available_members: prev.available_members.includes(memberName)
        ? prev.available_members.filter((name: string) => name !== memberName)
        : [...prev.available_members, memberName],
    }));
  };

  const handlePlanClick = (plan: EventPlan) => {
    setSelectedPlan(plan);
    setPlanDialogOpen(true);
  };

  const getThemeIcon = (theme: string) => {
    switch (theme) {
      case "fun 🎉":
        return <EmojiEvents />;
      case "chill 🧘":
        return <Nature />;
      case "outdoor 🌤":
        return <SportsEsports />;
      default:
        return <Group />;
    }
  };

  const getThemeColor = (theme: string) => {
    switch (theme) {
      case "fun 🎉":
        return "#ff6b6b";
      case "chill 🧘":
        return "#4ecdc4";
      case "outdoor 🌤":
        return "#45b7d1";
      default:
        return "#95a5a6";
    }
  };

  const renderEventPlanner = () => (
    <Container maxWidth='lg' sx={{ py: 4 }}>
      <Typography variant='h3' component='h1' gutterBottom align='center'>
        Team Bonding Event Planner
      </Typography>
      <Typography
        variant='h6'
        color='text.secondary'
        align='center'
        gutterBottom>
        Generate personalized team bonding plans based on member preferences
      </Typography>

      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant='h5' gutterBottom>
          Event Preferences
        </Typography>

        <Grid container spacing={3}>
          {/* Theme Selection */}
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Event Theme</InputLabel>
              <Select
                value={userPreferences.theme}
                label='Event Theme'
                onChange={(e: SelectChangeEvent) =>
                  setUserPreferences((prev: UserPreferences) => ({
                    ...prev,
                    theme: e.target.value,
                  }))
                }>
                <MenuItem value='fun 🎉'>Fun 🎉</MenuItem>
                <MenuItem value='chill 🧘'>Chill 🧘</MenuItem>
                <MenuItem value='outdoor 🌤'>Outdoor 🌤</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          {/* Budget Contribution */}
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Budget Contribution</InputLabel>
              <Select
                value={userPreferences.budget_contribution}
                label='Budget Contribution'
                onChange={(e: SelectChangeEvent) =>
                  setUserPreferences((prev: UserPreferences) => ({
                    ...prev,
                    budget_contribution: e.target.value,
                  }))
                }>
                <MenuItem value='No'>No additional contribution</MenuItem>
                <MenuItem value='Yes, up to 50,000 VND'>
                  Yes, up to 50,000 VND
                </MenuItem>
                <MenuItem value='Yes, up to 100,000 VND'>
                  Yes, up to 100,000 VND
                </MenuItem>
                <MenuItem value='Yes, up to 150,000 VND'>
                  Yes, up to 150,000 VND
                </MenuItem>
                <MenuItem value='Yes, up to 200,000 VND'>
                  Yes, up to 200,000 VND
                </MenuItem>
              </Select>
            </FormControl>
          </Grid>

          {/* Date and Time */}
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label='Preferred Date & Time'
              type='datetime-local'
              value={userPreferences.date_time}
              onChange={(e) =>
                setUserPreferences((prev: UserPreferences) => ({
                  ...prev,
                  date_time: e.target.value,
                }))
              }
              InputLabelProps={{
                shrink: true,
              }}
            />
          </Grid>

          {/* Location Zone */}
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label='Preferred Location Zone'
              placeholder='e.g., District 1'
              value={userPreferences.location_zone}
              onChange={(e) =>
                setUserPreferences((prev: UserPreferences) => ({
                  ...prev,
                  location_zone: e.target.value,
                }))
              }
            />
          </Grid>

          {/* Team Members */}
          <Grid item xs={12}>
            <Typography variant='h6' gutterBottom>
              Available Team Members
            </Typography>
            <FormGroup row>
              {teamMembers.map((member) => (
                <FormControlLabel
                  key={member.id}
                  control={
                    <Checkbox
                      checked={userPreferences.available_members.includes(
                        member.name
                      )}
                      onChange={() => handleMemberToggle(member.name)}
                    />
                  }
                  label={
                    <Box>
                      <Typography variant='body2'>{member.name}</Typography>
                      <Typography variant='caption' color='text.secondary'>
                        {member.vibe} • {member.location}
                      </Typography>
                    </Box>
                  }
                />
              ))}
            </FormGroup>
          </Grid>

          {/* Generate Button */}
          <Grid item xs={12}>
            <Button
              variant='contained'
              size='large'
              onClick={handleGeneratePlans}
              disabled={
                loading || userPreferences.available_members.length === 0
              }
              sx={{ mt: 2 }}
              fullWidth>
              {loading ? (
                <CircularProgress size={24} color='inherit' />
              ) : (
                "Generate Team Bonding Plans"
              )}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Error Display */}
      {error && (
        <Alert severity='error' sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {/* Generated Plans */}
      {plans.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant='h5' gutterBottom>
            Generated Plans ({plans.length})
          </Typography>
          <Grid container spacing={3}>
            {plans.map((plan, index) => (
              <Grid item xs={12} md={6} lg={4} key={index}>
                <Card
                  sx={{
                    height: "100%",
                    cursor: "pointer",
                    transition: "transform 0.2s",
                    "&:hover": {
                      transform: "translateY(-4px)",
                    },
                  }}
                  onClick={() => handlePlanClick(plan)}>
                  <CardContent>
                    <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                      <Box
                        sx={{
                          backgroundColor: getThemeColor(userPreferences.theme),
                          borderRadius: "50%",
                          p: 1,
                          mr: 2,
                        }}>
                        {getThemeIcon(userPreferences.theme)}
                      </Box>
                      <Typography variant='h6'>Plan {index + 1}</Typography>
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography
                        variant='body2'
                        color='text.secondary'
                        gutterBottom>
                        {plan.fit_analysis}
                      </Typography>
                    </Box>

                    <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                      <Rating value={plan.rating} readOnly size='small' />
                      <Typography variant='body2' sx={{ ml: 1 }}>
                        {plan.rating}/5
                      </Typography>
                    </Box>

                    <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                      <AttachMoney sx={{ mr: 1, color: "text.secondary" }} />
                      <Typography variant='body2'>
                        {plan.total_cost.toLocaleString()} VND
                      </Typography>
                    </Box>

                    {plan.contribution_needed > 0 && (
                      <Alert severity='warning' sx={{ mb: 2 }}>
                        Additional contribution:{" "}
                        {plan.contribution_needed.toLocaleString()} VND
                      </Alert>
                    )}

                    <Typography variant='body2' color='text.secondary'>
                      {plan.phases.length} phase
                      {plan.phases.length !== 1 ? "s" : ""}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Container>
  );

  return (
    <Container maxWidth='lg'>
      <Box sx={{ my: 4 }}>
        {/* Main Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: "divider", mb: 3 }}>
          <Tabs
            value={activeTab}
            onChange={(e, newValue) => setActiveTab(newValue)}>
            <Tab label='🎉 Event Planner' />
            <Tab label='👥 Team Members' />
            <Tab label='🤖 AI Management' />
          </Tabs>
        </Box>

        {/* Tab Content */}
        {activeTab === 0 && renderEventPlanner()}
        {activeTab === 1 && <TeamMemberManagement />}
        {activeTab === 2 && <AIManagement />}
      </Box>

      {/* Plan Detail Dialog */}
      <Dialog
        open={planDialogOpen}
        onClose={() => setPlanDialogOpen(false)}
        maxWidth='md'
        fullWidth>
        {selectedPlan && (
          <>
            <DialogTitle>
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Box
                  sx={{
                    backgroundColor: getThemeColor(userPreferences.theme),
                    borderRadius: "50%",
                    p: 1,
                    mr: 2,
                  }}>
                  {getThemeIcon(userPreferences.theme)}
                </Box>
                <Typography variant='h5' sx={{ fontWeight: "bold" }}>
                  Team Bonding Plan
                </Typography>
              </Box>
            </DialogTitle>

            <DialogContent>
              <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                  <Typography variant='h6' gutterBottom>
                    📍 Event Phases
                  </Typography>

                  {selectedPlan.phases.map(
                    (phase: EventPhase, index: number) => (
                      <Accordion key={index} sx={{ mb: 2 }}>
                        <AccordionSummary expandIcon={<ExpandMore />}>
                          <Box
                            sx={{
                              display: "flex",
                              alignItems: "center",
                              width: "100%",
                            }}>
                            <Typography variant='h6' sx={{ flexGrow: 1 }}>
                              Phase {index + 1}: {phase.activity}
                            </Typography>
                            <Chip
                              label={`${phase.cost.toLocaleString()} VND`}
                              color='primary'
                              size='small'
                            />
                          </Box>
                        </AccordionSummary>

                        <AccordionDetails>
                          <List dense>
                            <ListItem>
                              <ListItemIcon>
                                <LocationOn color='primary' />
                              </ListItemIcon>
                              <ListItemText
                                primary='Address'
                                secondary={phase.location}
                              />
                            </ListItem>

                            {phase.map_link && (
                              <ListItem>
                                <ListItemIcon>
                                  <Directions color='primary' />
                                </ListItemIcon>
                                <ListItemText
                                  primary='Google Maps'
                                  secondary={
                                    <a
                                      href={phase.map_link}
                                      target='_blank'
                                      rel='noopener noreferrer'>
                                      Open in Maps
                                    </a>
                                  }
                                />
                              </ListItem>
                            )}
                          </List>

                          <Box
                            sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                            {phase.indicators.map((indicator, idx) => (
                              <Chip
                                key={idx}
                                label={indicator}
                                size='small'
                                color={
                                  indicator === "indoor"
                                    ? "primary"
                                    : indicator === "outdoor"
                                    ? "secondary"
                                    : indicator === "vegetarian-friendly"
                                    ? "success"
                                    : indicator === "alcohol-friendly"
                                    ? "warning"
                                    : "default"
                                }
                              />
                            ))}
                          </Box>
                        </AccordionDetails>
                      </Accordion>
                    )
                  )}
                </Grid>

                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant='h6' gutterBottom>
                      💰 Cost Breakdown
                    </Typography>
                    <Typography
                      variant='h4'
                      sx={{ color: "#27ae60", fontWeight: "bold" }}>
                      {selectedPlan.total_cost.toLocaleString()} VND
                    </Typography>
                    <Typography variant='body2' sx={{ color: "#7f8c8d" }}>
                      per person
                    </Typography>
                    {selectedPlan.contribution_needed > 0 && (
                      <Alert severity='warning' sx={{ mt: 1 }}>
                        Additional contribution:{" "}
                        {selectedPlan.contribution_needed.toLocaleString()} VND
                      </Alert>
                    )}
                  </Paper>

                  <Paper sx={{ p: 2, mb: 2 }}>
                    <Typography variant='h6' gutterBottom>
                      👥 Team Fit
                    </Typography>
                    <Typography variant='body2' sx={{ color: "#7f8c8d" }}>
                      {selectedPlan.fit_analysis}
                    </Typography>
                    <Box sx={{ display: "flex", alignItems: "center", mt: 1 }}>
                      <Rating
                        value={selectedPlan.rating}
                        readOnly
                        size='small'
                      />
                      <Typography variant='body2' sx={{ ml: 1 }}>
                        {selectedPlan.rating}/5
                      </Typography>
                    </Box>
                  </Paper>
                </Grid>
              </Grid>
            </DialogContent>

            <DialogActions>
              <Button onClick={() => setPlanDialogOpen(false)}>Close</Button>
              <Button
                variant='contained'
                color='primary'
                onClick={() => {
                  // Here you could add functionality to save/export the plan
                  alert(
                    "Plan saved! (This would integrate with calendar/export features)"
                  );
                }}>
                Save Plan
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Container>
  );
}

export default App;
