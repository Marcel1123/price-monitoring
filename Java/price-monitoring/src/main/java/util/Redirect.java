package util;

import javax.faces.context.FacesContext;
import java.io.IOException;

public class Redirect {
    public static void redirectToIndex(){
        try {
            FacesContext.getCurrentInstance().getExternalContext().redirect("http://localhost:8080/price_monitoring_war/index.xhtml");
        } catch (IOException e) {
        }
    }
}
