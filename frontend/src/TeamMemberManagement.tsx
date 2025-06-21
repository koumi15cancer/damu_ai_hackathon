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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Grid,
  Alert,
} from "@mui/material";
import {
  Add,
  Edit,
  Delete,
  LocationOn,
  Psychology,
  Favorite,
} from "@mui/icons-material";
import axios from "axios";

interface TeamMember {
  id: string;
  name: string;
  location: string;
  preferences: string[];
  vibe: string;
}

interface NewTeamMember {
  name: string;
  location: string;
  preferences: string[];
  vibe: string;
}

function TeamMemberManagement() {
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [editingMember, setEditingMember] = useState<TeamMember | null>(null);
  const [newMember, setNewMember] = useState<NewTeamMember>({
    name: "",
    location: "",
    preferences: [],
    vibe: "Mixed",
  });

  const vibeOptions = ["Chill", "Energetic", "Mixed"];
  const preferenceOptions = [
    "Vegetarian",
    "Meat-lover",
    "BBQ",
    "Hotpot",
    "Karaoke",
    "Bar",
    "Cafe-hopping",
    "Games",
    "Outdoor walks",
    "Movie night",
    "Rooftop bar",
    "Dinner & chat",
    "Office snacks",
    "Asian food",
  ];

  useEffect(() => {
    loadTeamMembers();
  }, []);

  const loadTeamMembers = async () => {
    try {
      setLoading(true);
      const response = await axios.get("http://localhost:5000/team-members");
      setTeamMembers(response.data);
    } catch (error) {
      console.error("Failed to load team members:", error);
      setError(
        "Failed to load team members. Please check if the backend server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleAddMember = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        "http://localhost:5000/team-members",
        newMember
      );
      setTeamMembers([...teamMembers, response.data]);
      setDialogOpen(false);
      setNewMember({ name: "", location: "", preferences: [], vibe: "Mixed" });
    } catch (error) {
      console.error("Failed to add team member:", error);
      setError("Failed to add team member. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateMember = async () => {
    if (!editingMember) return;

    try {
      setLoading(true);
      const response = await axios.put(
        `http://localhost:5000/team-members/${editingMember.id}`,
        newMember
      );
      setTeamMembers(
        teamMembers.map((member) =>
          member.id === editingMember.id ? response.data : member
        )
      );
      setDialogOpen(false);
      setEditingMember(null);
      setNewMember({ name: "", location: "", preferences: [], vibe: "Mixed" });
    } catch (error) {
      console.error("Failed to update team member:", error);
      setError("Failed to update team member. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteMember = async (memberId: string) => {
    if (!window.confirm("Are you sure you want to delete this team member?"))
      return;

    try {
      setLoading(true);
      await axios.delete(`http://localhost:5000/team-members/${memberId}`);
      setTeamMembers(teamMembers.filter((member) => member.id !== memberId));
    } catch (error) {
      console.error("Failed to delete team member:", error);
      setError("Failed to delete team member. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const openEditDialog = (member: TeamMember) => {
    setEditingMember(member);
    setNewMember({
      name: member.name,
      location: member.location,
      preferences: member.preferences,
      vibe: member.vibe,
    });
    setDialogOpen(true);
  };

  const openAddDialog = () => {
    setEditingMember(null);
    setNewMember({ name: "", location: "", preferences: [], vibe: "Mixed" });
    setDialogOpen(true);
  };

  const handlePreferenceToggle = (preference: string) => {
    setNewMember((prev) => ({
      ...prev,
      preferences: prev.preferences.includes(preference)
        ? prev.preferences.filter((p) => p !== preference)
        : [...prev.preferences, preference],
    }));
  };

  const getVibeColor = (vibe: string) => {
    switch (vibe) {
      case "Chill":
        return "#4ecdc4";
      case "Energetic":
        return "#ff6b6b";
      case "Mixed":
        return "#95a5a6";
      default:
        return "#95a5a6";
    }
  };

  return (
    <Container maxWidth='lg' sx={{ py: 4 }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 4,
        }}>
        <Typography variant='h4' component='h1'>
          Team Member Management
        </Typography>
        <Button variant='contained' startIcon={<Add />} onClick={openAddDialog}>
          Add Member
        </Button>
      </Box>

      {error && (
        <Alert severity='error' sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {teamMembers.map((member) => (
          <Grid item xs={12} md={6} lg={4} key={member.id}>
            <Card>
              <CardContent>
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    mb: 2,
                  }}>
                  <Typography variant='h6' component='h2'>
                    {member.name}
                  </Typography>
                  <Box>
                    <IconButton
                      size='small'
                      onClick={() => openEditDialog(member)}
                      sx={{ mr: 1 }}>
                      <Edit />
                    </IconButton>
                    <IconButton
                      size='small'
                      color='error'
                      onClick={() => handleDeleteMember(member.id)}>
                      <Delete />
                    </IconButton>
                  </Box>
                </Box>

                <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                  <LocationOn sx={{ mr: 1, color: "text.secondary" }} />
                  <Typography variant='body2' color='text.secondary'>
                    {member.location}
                  </Typography>
                </Box>

                <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                  <Psychology sx={{ mr: 1, color: "text.secondary" }} />
                  <Chip
                    label={member.vibe}
                    size='small'
                    sx={{
                      backgroundColor: getVibeColor(member.vibe),
                      color: "white",
                    }}
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography
                    variant='body2'
                    color='text.secondary'
                    gutterBottom>
                    Preferences:
                  </Typography>
                  <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                    {member.preferences.map((preference, index) => (
                      <Chip
                        key={index}
                        label={preference}
                        size='small'
                        icon={<Favorite />}
                        variant='outlined'
                      />
                    ))}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Add/Edit Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth='sm'
        fullWidth>
        <DialogTitle>
          {editingMember ? "Edit Team Member" : "Add New Team Member"}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <TextField
              fullWidth
              label='Name'
              value={newMember.name}
              onChange={(e) =>
                setNewMember({ ...newMember, name: e.target.value })
              }
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              label='Location'
              value={newMember.location}
              onChange={(e) =>
                setNewMember({ ...newMember, location: e.target.value })
              }
              sx={{ mb: 2 }}
            />

            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Vibe</InputLabel>
              <Select
                value={newMember.vibe}
                label='Vibe'
                onChange={(e) =>
                  setNewMember({ ...newMember, vibe: e.target.value })
                }>
                {vibeOptions.map((vibe) => (
                  <MenuItem key={vibe} value={vibe}>
                    {vibe}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Typography variant='body2' color='text.secondary' gutterBottom>
              Preferences:
            </Typography>
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5, mb: 2 }}>
              {preferenceOptions.map((preference) => (
                <Chip
                  key={preference}
                  label={preference}
                  size='small'
                  onClick={() => handlePreferenceToggle(preference)}
                  color={
                    newMember.preferences.includes(preference)
                      ? "primary"
                      : "default"
                  }
                  variant={
                    newMember.preferences.includes(preference)
                      ? "filled"
                      : "outlined"
                  }
                />
              ))}
            </Box>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            variant='contained'
            onClick={editingMember ? handleUpdateMember : handleAddMember}
            disabled={loading || !newMember.name || !newMember.location}>
            {editingMember ? "Update" : "Add"}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default TeamMemberManagement;
