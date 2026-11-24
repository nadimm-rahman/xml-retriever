import oracledb
import xml.etree.ElementTree as ET
from pathlib import Path

# --------------------------------------------------
# DATABASE CONNECTION DETAILS
# --------------------------------------------------

DB_USER = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = XXXX
DB_SERVICE = ""

# --------------------------------------------------
# EXPERIMENT IDS TO RETRIEVE
# --------------------------------------------------

# ======================================================= #
experiment_ids = ['XXXXX', 'XXXXX'...]  # Needs updating per script run

OUTPUT_FILE = "experiment_set.xml"
# ======================================================= #

def export_experiments(experiment_ids, output_file):

    if not experiment_ids:
        raise ValueError("No experiment IDs provided.")

    # Establish Oracle connection
    connection = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        service_name=DB_SERVICE
    )

    try:
        cursor = connection.cursor()

        # Create bind variables for the IN clause
        bind_params = {
            f"id{i}": experiment_id
            for i, experiment_id in enumerate(experiment_ids)
        }

        # Generate placeholders
        placeholders = ", ".join(
            f":{key}" for key in bind_params
        )

        # ======================================================= #
        # SQL query - XMLSERIALIZE converts Oracle XMLTYPE to CLOB
        # EDIT THE SQL QUERY BEFORE RUNNING TO GET THE APPROPRIATE XML OBJECTS #
        sql = f"""
            SELECT
                id,
                XMLSERIALIZE(
                    CONTENT xml_column AS CLOB
                ) AS xml_column_name
            FROM table
            WHERE id IN (SELECT id FROM table_name WHERE table_name_ids in ({placeholders}))
            ORDER BY id
        """
        # ======================================================= #

        cursor.execute(sql, bind_params)
        # cursor.execute(sql, experiment_ids)

        # Create root XML element
        root = ET.Element("EXPERIMENT_SET")

        count = 0

        for experiment_id, xml_data in cursor:

            if xml_data is None:
                continue

            # Oracle CLOB may need to be read
            if hasattr(xml_data, "read"):
                xml_data = xml_data.read()

            # Parse the XML
            experiment_element = ET.fromstring(xml_data.strip())

            if experiment_element.tag == "EXPERIMENT":
                # Append to the root
                root.append(experiment_element)
                count += 1

            elif experiment_element.tag == "EXPERIMENT_SET":

                # Extract individual EXPERIMENT blocks without retaining the existing wrapper
                for experiment in experiment_element.findall("EXPERIMENT"):
                    root.append(experiment)
                    count += 1

            else:
                raise ValueError(
                    f"Unexpected XML root '{experiment_element.tag}' "
                    f"for experiment ID {experiment_id}"
                )

            print(f"Retrieved experiment: {experiment_id}")

        # Write final XML file
        tree = ET.ElementTree(root)

        ET.indent(tree, space="  ", level=0)

        tree.write(
            output_file,
            encoding="utf-8",
            xml_declaration=True
        )

        print(f"\nSuccessfully exported {count} experiments.")
        print(f"Output file: {Path(output_file).resolve()}")

    finally:
        connection.close()


if __name__ == "__main__":
    export_experiments(experiment_ids, OUTPUT_FILE)
