from odbAccess import *
from abaqusConstants import INTEGRATION_POINT 
import csv

# Path to the ODB file
odb_path = r'C:\Users\admin\Desktop\navankur\test case\with SDV\Job-eqplastic.odb'

# Open the ODB file
odb = openOdb(path=odb_path)

# Define step name and node set name
step_name = 'Step-1'
node_set_name = ' ALL NODES'
element_set_name = ' ALL ELEMENTS'

# Get the step object
step = odb.steps[step_name]

# Print node sets in the root assembly
# print("Node Sets in Root Assembly:")
# for node_set_name in odb.rootAssembly.nodeSets.keys():
#     print("  -", node_set_name)

# # Print node sets for each instance in the assembly
# print("\nNode Sets in Instances:")
# for instance_name, instance in odb.rootAssembly.instances.items():
#     print("Instance:", instance_name)
#     for node_set_name in instance.nodeSets.keys():
#         print("  -", node_set_name)


# Get the node set object
# node_set = odb.rootAssembly.nodeSets[node_set_name]
element_set = odb.rootAssembly.elementSets[element_set_name]

# Function to compute sum manually
def manual_sum(values):
    total = 0
    for val in values:
        total += val
    return total

# Initialize lists to store averaged values
averaged_s11 = []
averaged_le11 = []

# Loop through all frames in the step
for frame_idx, frame in enumerate(step.frames):
    # Access field outputs for stress (S) and logarithmic strain (LE)
    s_field = frame.fieldOutputs['S']
    le_field = frame.fieldOutputs['SDV1'] #PEEQ

    # Extract values specifically for the given node set
    s_subset = s_field.getSubset(region=element_set)
    le_subset = le_field.getSubset(region=element_set)

    # Extract S11 and LE11 values
    s11_values = [s.mises for s in s_subset.values]  # First component (S11)
    le11_values = [le.data for le in le_subset.values]  # First component (LE11)
    # Calculate sums using a loop
    total_s11 = manual_sum(s11_values)
    total_le11 = manual_sum(le11_values)

    # # Calculate averages manually
    # avg_s11 = total_s11 / len(s11_values) 
    # avg_le11 = total_le11 / len(le11_values) 

    if not s11_values:
        print("Warning: No S11 values found for frame", frame_idx)
        avg_s11 = 0
    else:
        total_s11 = manual_sum(s11_values)
        avg_s11 = total_s11 / len(s11_values)

    if not le11_values:
        print("Warning: No LE11 values found for frame", frame_idx)
        avg_le11 = 0
    else:
        total_le11 = manual_sum(le11_values)
        avg_le11 = total_le11 / len(le11_values)

    # Store results
    averaged_s11.append(avg_s11)
    averaged_le11.append(avg_le11)

# Save results to a CSV file
output_csv_path = r'C:\Users\admin\Desktop\navankur\test case\with SDV\averaged_results.csv'
with open(output_csv_path, mode='w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Frame', 'Average Smises', 'Average PEEQ'])
    for i, (s11, le11) in enumerate(zip(averaged_s11, averaged_le11)):
        writer.writerow([i + 1, s11, le11])

print("Averaged results saved to {}".format(output_csv_path))
total_frames = len(averaged_s11)
print("Total Frames Processed:", total_frames)
print("Final Average SMISES:", averaged_s11[-1] if averaged_s11 else "No Data")
print("Final Average PEEQ:", averaged_le11[-1] if averaged_le11 else "No Data")
