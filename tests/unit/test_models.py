from ai_company.models.models import Executive


def test_executive():

    executive = Executive(

        id="cto",

        title="Chief Technology Officer",

        department="Technology",

        reports_to="chief-of-staff",

        role="Technology Executive",

        mission="Build the technology strategy."

    )

    print(executive)

    assert executive.id == "cto"

    assert executive.department == "Technology"