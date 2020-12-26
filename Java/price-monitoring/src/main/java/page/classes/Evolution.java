package page.classes;

import entities.ProductEntity;
import lombok.Getter;
import lombok.Setter;

import javax.annotation.PostConstruct;
import javax.enterprise.context.RequestScoped;
import javax.faces.context.FacesContext;
import javax.inject.Named;
import java.util.Map;

@Named
@RequestScoped
@Getter
@Setter
public class Evolution {
    private ProductEntity productEntity;

    @PostConstruct
    public void init(){
        Map<String, Object> parameterValue = FacesContext.getCurrentInstance().getExternalContext().getSessionMap();
        productEntity = (ProductEntity) parameterValue.get("product_for_evaluation");
    }
}
