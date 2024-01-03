from pandas import DataFrame

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def generate_email_body(df: DataFrame, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    if df.empty:
        email_body = "Hi user! There is no updates for today."
        return email_body

    grouped = df.groupby(["source", "job_status"])

    email_body = "Hi, user!\nHere is the list of updates of the job listings for the companies you are following:\n"

    for (source, job_status), group in grouped:
        email_body += f"{source}:\n"
        if job_status == "Position opened":
            email_body += "    Opened positions:\n"
            for _, row in group.iterrows():
                location = (
                    f"remote ({row['job_location']})"
                    if row["remote"] == "true"
                    else f"On-site in {row['job_location']}"
                )
                email_body += f"        {row['title']}: {row['department']} in {row['company']}, {location} ({row['absolute_url']})\n"
        else:
            email_body += "    Closed positions:\n"
            for _, row in group.iterrows():
                email_body += (
                    f"        {row['title']}: {row['department']} in {row['company']}\n"
                )

    return email_body
