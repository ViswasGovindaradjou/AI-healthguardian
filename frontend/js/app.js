const API_URL = "http://127.0.0.1:8000/analyze-report";

const analyzeBtn =
    document.getElementById("analyzeBtn");

analyzeBtn.addEventListener(
    "click",
    async () => {

        const file =
            document.getElementById(
                "reportFile"
            ).files[0];

        if (!file) {

            alert(
                "Please select a PDF report"
            );

            return;
        }

        document.getElementById(
            "loading"
        ).style.display = "block";

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        try {

            const response =
                await fetch(
                    API_URL,
                    {
                        method: "POST",
                        body: formData
                    }
                );

            const data =
                await response.json();

            displayResults(data);

        } catch (err) {

            alert(
                "Error connecting to backend"
            );

            console.log(err);

        }

        document.getElementById(
            "loading"
        ).style.display = "none";
    }
);


function getRiskClass(risk) {

    if (risk <= 30)
        return "low";

    if (risk <= 70)
        return "medium";

    return "high";
}


function createCard(
    name,
    risk,
    source
) {

    const riskClass =
        getRiskClass(risk);

    return `
        <div class="card ${riskClass}">
            <h3>${name}</h3>
            <p><b>${risk}%</b></p>
            <p>${source}</p>
        </div>
    `;
}


function displayResults(
    data
) {

    document.getElementById(
        "patientProfile"
    ).style.display = "block";

    document.getElementById(
        "riskCards"
    ).style.display = "block";

    document.getElementById(
        "reportSection"
    ).style.display = "block";

    document.getElementById(
        "profileData"
    ).textContent =
        JSON.stringify(
            data.patient_profile,
            null,
            4
        );

    const results =
        data.results;

    document.getElementById(
        "diabetesCard"
    ).innerHTML =
        createCard(
            "Diabetes",
            results.diabetes.risk,
            results.diabetes.source
        );

    document.getElementById(
        "heartCard"
    ).innerHTML =
        createCard(
            "Heart",
            results.heart.risk,
            results.heart.source
        );

    document.getElementById(
        "kidneyCard"
    ).innerHTML =
        createCard(
            "Kidney",
            results.kidney.risk,
            results.kidney.source
        );

    document.getElementById(
        "liverCard"
    ).innerHTML =
        createCard(
            "Liver",
            results.liver.risk,
            results.liver.source
        );

    document.getElementById(
        "strokeCard"
    ).innerHTML =
        createCard(
            "Stroke",
            results.stroke.risk,
            results.stroke.source
        );

    document.getElementById(
        "finalReport"
    ).textContent =
        data.final_report;
}